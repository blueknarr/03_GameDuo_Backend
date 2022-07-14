from django.contrib import admin
from django.urls import path, include
from user.views import UserApi

urlpatterns = [
    path('users/', UserApi.as_view()),
    path('users/<int:user_id>', UserApi.as_view())
]