from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User, Permission, Group
from jwt import get_unverified_header, decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidAudienceError, DecodeError, \
    InvalidIssuerError
import requests
from cryptography.x509 import load_pem_x509_certificate
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import DjangoModelPermissions


def is_token_expired(token):
    # used to check if a Token has expired based on the TOKEN_EXPIRED_AFTER_SECONDS setting
    # token: rest_framework.authtoken.models.Token
    time_elapsed = timezone.now() - token.created
    time_left = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return time_left < timedelta(seconds=0)


class AzureAuthentication(BaseAuthentication):
    """
    A custom authentication scheme for validating an Azure access token

    Description:
    * Validate the Azure access token, if valid create a user if they do not exist
      and set/check/update their permissions or groups based on the roles in the Azure access token.
    * see  https://pyjwt.readthedocs.io/en/stable/api.html for documentation on the validation process

    NOTE:
    * Values used to Verify the azure access token, set in settings.py
        - AZURE_AUTH_TYPE_PREFIX = 'Bearer'
        - AZURE_AUDIENCE = "api://f7e456dd-39f4-4a2f-b068-81bff33ff0d3"
        - AZURE_ALLOWED_ALGORITHMS = ['RS256']
        - AZURE_ISSUER = "https://sts.windows.net/459d0de0-228b-41cf-99bf-e12106d5de82/"
    * We do not want to compute these from the incoming access token,
      that would expose vulnerabilities (see RFC 8725 S2.1)

    """

    def authenticate(self, request):
        # parse the access token from the auth header
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        # if auth header is not found then end authentication
        if not authorization_header:
            return None

        # make sure the proper prefix was used
        bearer, _, token = authorization_header.partition(' ')
        if bearer != settings.AZURE_AUTH_TYPE_PREFIX:
            raise AuthenticationFailed("Invalid token.")

        try:
            decoded_jwt = self.validate_accesstoken(token)
        except ExpiredSignatureError as err:
            raise AuthenticationFailed("Token has expired")
        except (InvalidSignatureError, InvalidAudienceError, DecodeError, InvalidIssuerError) as err:
            raise AuthenticationFailed('Invalid token.')

        # create a user with their email if they do not exist and check/update permissions
        # the email and username need to match and are case sensitive
        # user (object), created (boolean)
        user, user_created = User.objects.get_or_create(
            username=decoded_jwt["unique_name"].lower(),
            last_name=decoded_jwt["family_name"].lower(),
            first_name=decoded_jwt["given_name"].lower(),
            email=decoded_jwt["unique_name"].lower()
        )

        # if a user already exists check if the token has expired
        if not user_created:
            drf_token = Token.objects.get(user=user)
            # if the token has expired then delete it and create a new one
            if is_token_expired(drf_token):
                drf_token.delete()
                Token.objects.create(user=user)

        self.assign_permissions_and_groups(decoded_jwt, user, user_created)

        return (user, None)

    def validate_accesstoken(self, access_token):
        # find the kid that will be used to find the public key
        kid = get_unverified_header(access_token)['kid']
        # get the public key from azure jwks uri endpount
        res = requests.get(settings.AZURE_OPENID_CONFIG)
        jwk_uri = res.json()["jwks_uri"]

        # get all of the jwk keys from azure
        res = requests.get(jwk_uri)
        jwk_keys = res.json()

        # find which key matches our kid
        x5c = None
        for key in jwk_keys['keys']:
            if key['kid'] == kid:
                x5c = key['x5c']

        # create the certificate
        cert = ''.join([
            '-----BEGIN CERTIFICATE-----\n',
            x5c[0],
            '\n-----END CERTIFICATE-----\n',
        ])

        # load the public key
        public_key = load_pem_x509_certificate(cert.encode()).public_key()
        # decode and verify the jwt (will handle validation and expiration check)
        decoded_jwt = decode(
            access_token,
            public_key,
            algorithms=settings.AZURE_ALLOWED_ALGORITHMS,
            audience=settings.AZURE_AUDIENCE,
            issuer=settings.AZURE_ISSUER
        )
        return decoded_jwt

    def assign_permissions_and_groups(self, decoded_jwt, user, user_created):
        # roles created in Azure AD need to exactly match the Django permission code names or group names
        # perm_ids need to be a list of permission id's based on the auth_permission table
        # group_ids need to be a list of group id's based on the auth_group table
        # see https://docs.djangoproject.com/en/3.2/topics/auth/default/#permissions-and-authorization
        if 'roles' in decoded_jwt and user_created:
            # new user was created, so set the permissions and groups
            perm_ids, group_ids = self.get_perm_and_group_ids(decoded_jwt["roles"])
            user.user_permissions.set(perm_ids)
            user.groups.set(group_ids)
        elif 'roles' in decoded_jwt and not user_created:
            # existing user and permission need to be checked/updated
            perm_ids, group_ids = self.get_perm_and_group_ids(decoded_jwt["roles"])
            user_perms = sorted([perm.id for perm in user.user_permissions.all()])
            user_groups = sorted([group.id for group in user.groups.all()])
            # update the permissions and groups if they do not match, or create set them if the user has none
            if perm_ids != user_perms:
                user.user_permissions.set(perm_ids)

            if group_ids != user_groups:
                user.groups.set(group_ids)

        elif 'roles' not in decoded_jwt and not user_created:
            # existing user and the user has no permissions or groups
            # clear permissions and groups if they currently have permissions
            if len(user.get_user_permissions()) > 0:
                user.user_permissions.clear()

            if len(user.get_group_permissions()) > 0:
                user.groups.clear()

    def get_perm_and_group_ids(self, roles):
        # Get the permission and group id's from the auth_permission table and auth_group table respectively
        # sort the id's in ascending order
        permissions = Permission.objects.filter(codename__in=roles)
        groups = Group.objects.filter(name__in=roles)
        perm_ids = sorted([permission.id for permission in permissions])
        group_ids = sorted([group.id for group in groups])
        return perm_ids, group_ids


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Extending the Token Authentication Backend to expire the rest_framework.authtoken.models.Token model

    Description:
    * only need to override the authenticate_credentials method
    * the token will expire {n} seconds after creation,
      based on the TOKEN_EXPIRED_AFTER_SECONDS configuration in settings.py

    NOTE:
    * this is designed initially to be used in tandem with the Azure AD OAuth2.0 Authorization Code FLow
    * got idea from
      https://idiomaticprogrammers.com/post/how-to-implement-auto-expiring-token-in-django-rest-framework/#fn-2
    """

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        if is_token_expired(token):
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)


class DjangoModelPermissionsExtended(DjangoModelPermissions):
    # Map methods into required permission codes.
    # Override the perms_map attribute so that the 'GET' uses the 'view' permissions, see source code
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
