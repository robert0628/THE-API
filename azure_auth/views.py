from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .authentication import AzureAuthentication


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # automatically generate a auth token when user is created
    if created:
        Token.objects.create(user=instance)


# Create your views here.
class AuthAPIView(APIView):
    # this auth class will override the ExpiringTokenAuthentication in settings.py
    authentication_classes = [AzureAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        drf_token = Token.objects.get(user=request.user).key
        users_name = user.first_name + " " + user.last_name
        users_permissions = user.get_group_permissions() | user.get_user_permissions()
        return Response({'token': drf_token, 'user': users_name, 'permissions': users_permissions})


class CheckExpTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users_name = request.user.first_name + " " + request.user.last_name
        return Response({'user': users_name, 'isExpired': False})
