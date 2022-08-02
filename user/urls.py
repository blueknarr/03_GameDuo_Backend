from django.contrib import admin
from django.urls import path, include
from user.views import UserApi

urlpatterns = [
    path('', UserApi.as_view()),
    path('<int:user_id>/', UserApi.as_view())
]