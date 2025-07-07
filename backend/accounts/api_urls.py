from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import MeView

urlpatterns = [
    path("me/", MeView.as_view()),
]
