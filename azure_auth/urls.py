from django.urls import path
from .views import AuthAPIView, CheckExpTokenView

urlpatterns = [
    path('azure_oauth2/', AuthAPIView.as_view()),
    path('token_check/', CheckExpTokenView.as_view())
]