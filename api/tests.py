from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer


class UsersApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_superuser(username='admin')
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.client_admin = self.client_class()
        self.client_not_auth = self.client_class()

        self.client_admin.force_authenticate(self.user_admin)
        self.client.force_authenticate(self.user_1)

    def test_registration(self):
        """Регистрация пользователя."""
        self.assertEqual(3, User.objects.all().count())
        url = reverse('registration')

        data = {'username': 'user_created', 'password': '12qw$tuAS'}
        response = self.client_not_auth.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, User.objects.all().count())
        new_user = User.objects.all().last()
        self.assertEqual('user_created', new_user.username)

    def test_token(self):
        """Получение токена и авторизация с помощью токена."""
        url_reg = reverse('registration')
        data = {'username': 'user_created', 'password': '12qw$tuAS'}
        response = self.client_not_auth.post(url_reg, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        user = User.objects.all().last()

        url_token = reverse('token')
        data = {'username': user.username, 'password': '12qw$tuAS'}
        response = self.client.post(url_token, data=data)
        token = response.data['token']

        url = reverse('users-list')
        client = self.client_not_auth
        response_not_auth = client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         response_not_auth.status_code)

        client.force_authenticate(user=user, token=token)
        response_users_list = client.get(url)
        self.assertEqual(status.HTTP_200_OK, response_users_list.status_code)

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
        data = {'username': 'user_3'}
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

    def test_update(self):
        """Администратор редактирует пользователя."""
        old_user = {
            'username': self.user_2.username,
            'is_staff': self.user_2.is_staff,
        }
        url = reverse('users-detail', args=(self.user_2.id,))
        data = {'username': 'new_name', 'is_staff': True, 'first_name': 'yyy'}
        response = self.client_admin.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_2.refresh_from_db()
        self.assertNotEqual(old_user['username'], self.user_2.username)
        self.assertNotEqual(old_user['is_staff'], self.user_2.is_staff)
        self.assertEqual('new_name', self.user_2.username)
        self.assertEqual('yyy', self.user_2.first_name)

    def test_update_user(self):
        """Пользователь редактирует свои данные."""
        old_user = {
            'username': self.user_1.username,
            'first_name': self.user_1.first_name,
            'is_staff': self.user_1.is_staff,
        }
        url = reverse('users-detail', args=(self.user_1.id,))
        data = {'username': 'new_name', 'first_name': 'yyy', 'is_staff': True}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_1.refresh_from_db()
        self.assertNotEqual(old_user['username'], self.user_1.username)
        self.assertNotEqual(old_user['first_name'], self.user_1.first_name)
        self.assertEqual(old_user['is_staff'], self.user_1.is_staff)
        self.assertEqual('new_name', self.user_1.username)
        self.assertEqual('yyy', self.user_1.first_name)

    def test_update_any_user(self):
        """Пользователь не может редактировать данные другого пользователя."""
        old_user = {
            'username': self.user_2.username,
            'first_name': self.user_2.first_name,
            'is_staff': self.user_2.is_staff,
        }
        url = reverse('users-detail', args=(self.user_2.id,))
        data = {'username': 'new_name', 'first_name': 'yyy', 'is_staff': True}
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.user_2.refresh_from_db()
        self.assertEqual(old_user['username'], self.user_2.username)
        self.assertEqual(old_user['first_name'], self.user_2.first_name)
        self.assertEqual(old_user['is_staff'], self.user_2.is_staff)
        self.assertNotEqual('new_name', self.user_2.username)
        self.assertNotEqual('yyy', self.user_2.first_name)

    def test_delete(self):
        """Админ может удалить пользователя."""
        self.assertEqual(3, User.objects.all().count())
        url = reverse('users-detail', args=(self.user_2.id,))
        response = self.client_admin.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, User.objects.all().count())

    def test_delete_user(self):
        """Пользователь может удалить свои данные."""
        self.assertEqual(3, User.objects.all().count())
        url = reverse('users-detail', args=(self.user_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, User.objects.all().count())

    def test_delete_any_user(self):
        """Пользователь не может удалить другого пользователя."""
        self.assertEqual(3, User.objects.all().count())
        url = reverse('users-detail', args=(self.user_2.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, User.objects.all().count())
