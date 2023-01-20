from _ast import pattern
from authentication.views import  RegisterAPIView
from django.urls import path


urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
]