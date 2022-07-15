from django.contrib import admin
from django.urls import path, include
from bossraid.views import RaidStartApi, RaidEndApi

urlpatterns = [
    path('start/', RaidStartApi.as_view()),
    path('end/', RaidEndApi.as_view())
]