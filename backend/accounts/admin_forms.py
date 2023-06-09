from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "name")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

        