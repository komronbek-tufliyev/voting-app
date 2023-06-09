""" 
    Generate Swagger API documentation 
    for the backend project.

    This file is used to generate Swagger API documentation for the backend project.
    It is not used by the backend project itself.
"""
from django.urls import path
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    UserDeleteAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserPasswordResetAPIView,
    UserChangePasswordAPIView,
)


urlpatterns = [
    # Get requests
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),

    # Post requests
    path("users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
    path("users/login/", UserLoginAPIView.as_view(), name="user-login"),
    path("users/logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("users/password/reset/", UserPasswordResetAPIView.as_view(), name="user-password-reset"),
    path("users/password/change/", UserChangePasswordAPIView.as_view(), name="user-change-password"),
]