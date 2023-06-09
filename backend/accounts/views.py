from rest_framework import views, status, generics, permissions
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserPasswordResetSerializer,
    UserChangePasswordSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    UserDeleteSerializer,
)

class UserListAPIView(generics.ListAPIView):
    """
    API view for user list.
    """
    queryset = UserSerializer.Meta.model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, permissions.IsAuthenticated, )

class UserCreateAPIView(generics.CreateAPIView):
    """
    API view for user create.
    """
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny, )

class UserLoginAPIView(views.APIView):
    """
    API view for user login.
    """
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user"]
        token = user.get_token()
        return Response({"token": token}, status=status.HTTP_200_OK)
    
class UserLogoutAPIView(views.APIView):
    """
    API view for user logout.
    """
    serializer_class = UserLogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserPasswordResetAPIView(views.APIView):
    """
    API view for user password reset.
    """
    serializer_class = UserPasswordResetSerializer
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserChangePasswordAPIView(views.APIView):
    """
    API view for user change password.
    """
    serializer_class = UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self):
        return self.request.user
    
class UserDetailAPIView(generics.RetrieveAPIView):
    """
    API view for user detail.
    """
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserSerializer.Meta.model.objects.all()
    
    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)
    
class UserUpdateAPIView(generics.UpdateAPIView):
    """
    API view for user update.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserSerializer.Meta.model.objects.all()
    
    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)
    
class UserDeleteAPIView(generics.DestroyAPIView):
    """
    API view for user delete.
    """
    serializer_class = UserDeleteSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserSerializer.Meta.model.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk)
    
    def get_object(self):
        return self.request.user
    