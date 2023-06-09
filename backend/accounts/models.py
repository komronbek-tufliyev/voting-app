from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    # base fields
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=100, blank=True)

    # for admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    #  activity tracking
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # for custom user manager
    objects = CustomUserManager()

    # some methods
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.name:
            return self.name
        return self.email
    