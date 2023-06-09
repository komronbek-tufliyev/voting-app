from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user list API.
    """
    class Meta:
        model = User
        fields = ("id", "email", "name", "is_staff", "is_active", "date_joined", "last_login")
        read_only_fields = ("id", "is_staff", "is_active", "date_joined", "last_login")

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user create API.

    Requires email and password both.
    """
    class Meta:
        model = User
        fields = ("id", "email", "name", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login API.

    Returns token if user is active and authenticated.
    Requires email and password both.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = _("User is not active.")
                    raise serializers.ValidationError(msg)
            else:
                msg = _("Unable to login with given credentials.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must provide email and password both.")
            raise serializers.ValidationError(msg)
        return data
    
class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for user detail API.
    """
    class Meta:
        model = User
        fields = ("id", "email", "name", "is_staff", "is_active", "date_joined", "last_login")
        read_only_fields = ("id", "email", "is_staff", "is_active", "date_joined", "last_login")

class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for user password reset API.

    Requires email.
    """
    email = serializers.EmailField()
    
    def validate(self, data):
        email = data.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
                data["user"] = user
            except User.DoesNotExist:
                msg = _("User does not exist.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must provide email.")
            raise serializers.ValidationError(msg)
        return data
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update API.

    Requires name.
    """
    class Meta:
        model = User
        fields = ("id", "email", "name")
        read_only_fields = ("id", "email")
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for user change password API.

    Requires old_password and new_password both.
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    
    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        if old_password and new_password:
            user = self.context.get("request").user
            if user.check_password(old_password):
                if old_password == new_password:
                    msg = _("New password must be different from old password.")
                    raise serializers.ValidationError(msg)
            else:
                msg = _("Old password is incorrect.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must provide old_password and new_password both.")
            raise serializers.ValidationError(msg)
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
    
class UserChangeNameSerializer(serializers.Serializer):
    """
    Serializer for user change name API.

    Requires name.
    """
    name = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance
    
class UserChangeEmailSerializer(serializers.Serializer):
    """
    Serializer for user change email API.

    Requires email.
    """
    email = serializers.EmailField()
    
    def validate(self, data):
        email = data.get("email")
        if email:
            if User.objects.filter(email=email).exists():
                msg = _("Email already exists.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must provide email.")
            raise serializers.ValidationError(msg)
        return data
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email")
        instance.save()
        return instance
    
class UserChangePasswordByAdminSerializer(serializers.Serializer):
    """
    Serializer for user change password by admin API.

    Requires new_password.
    """
    new_password = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
    
class UserChangeNameByAdminSerializer(serializers.Serializer):
    """
    Serializer for user change name by admin API.

    Requires name.
    """
    name = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance
    
class UserChangeEmailByAdminSerializer(serializers.Serializer):
    """
    Serializer for user change email by admin API.

    Requires email.
    """
    email = serializers.EmailField()
    
    def validate(self, data):
        email = data.get("email")
        if email:
            if User.objects.filter(email=email).exists():
                msg = _("Email already exists.")
                raise serializers.ValidationError(msg)
        else:
            msg = _("Must provide email.")
            raise serializers.ValidationError(msg)
        return data
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email")
        instance.save()
        return instance
    
class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout API.

    Requires nothing.
    """
    def validate(self, data):
        user = self.context.get("request").user
        if user:
            data["user"] = user
        else:
            msg = _("User is not authenticated.")
            raise serializers.ValidationError(msg)
        return data
    
class UserDeleteSerializer(serializers.Serializer):
    """
    Serializer for user delete API.

    Requires nothing.
    """
    def validate(self, data):
        user = self.context.get("request").user
        if user:
            data["user"] = user
        else:
            msg = _("User is not authenticated.")
            raise serializers.ValidationError(msg)
        return data
    
class UserInactivateSerializer(serializers.Serializer):
    """
    Serializer for user inactivate API.

    Requires nothing.
    """
    def validate(self, data):
        user = self.context.get("request").user
        if user:
            data["user"] = user
        else:
            msg = _("User is not authenticated.")
            raise serializers.ValidationError(msg)
        return data