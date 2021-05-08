from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import User
from .permissions import ProjectPermission
from .serializers import UserSerializer, UserRegSerializer, UserAdminSerializer


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegSerializer


class UserViewSet(ModelViewSet):
    """Пользователи."""
    queryset = User.objects.all()
    permission_classes = (ProjectPermission, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserAdminSerializer
        return UserSerializer
