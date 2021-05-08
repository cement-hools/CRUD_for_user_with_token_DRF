from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer


class UsersApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_superuser(username='admin')
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        # Token.objects.create(user=self.user_admin)
        # token = Token.objects.get(user=self.user_admin)
        # print(token)

        self.client_admin = self.client_class()

        self.client_admin.force_authenticate(self.user_admin)
        self.client.force_authenticate(self.user_1)

    def test_get_list(self):
        """Список всех пользователей."""
        url = reverse('users-list')
        users = User.objects.all()
        response = self.client.get(url)
        serializer_data = UserSerializer(users, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_detail(self):
        """Пользователь."""
        url = reverse('users-detail', args=(self.user_admin.id,))
        response = self.client.get(url)
        serializer_data = UserSerializer(self.user_admin).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        """Создание пользователя."""
        self.assertEqual(3, User.objects.all().count())
        data = {"username": "user_3"}
        url = reverse('users-list')

        response = self.client_admin.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, User.objects.all().count())
        new_user = User.objects.all().last()
        serializer_data = UserSerializer(new_user).data

        self.assertEqual(response.data, serializer_data)

    def test_create_not_admin(self):
        """Не админ не может создать пользователя."""
        data = {"username": "user_3"}
        url = reverse('users-list')
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
