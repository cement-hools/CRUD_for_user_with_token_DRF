from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserRegSerializer(ModelSerializer):
    """Сериалайзер регистрации."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password',)

    def create(self, validated_data):
        """Сохранение пользователи в модели User."""
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(ModelSerializer):
    """Сериалайзер пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'date_joined',)
        read_only_fields = ('date_joined', 'is_staff',)


class UserAdminSerializer(ModelSerializer):
    """Сериалайзер пользователей администратора."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'date_joined',)
        read_only_fields = ('date_joined',)
