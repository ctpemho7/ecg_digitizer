from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import UserModel

user_data = {
    "username": "fofo",
    "first_name": "Fofo",
    "last_name": "Fofo",
    "email": "yandex@yandex.ru",
    "status": "P",
    "password": "12345678"
}


class UserTests(APITestCase):
    def test_create_account(self):
        """
        Создать пользователя.
        """
        url = reverse('usermodel-list')

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(UserModel.objects.get().first_name, 'Fofo')

    def test_get_account(self):
        """
        Получить пользователя.
        """
        # создать пользователя
        url = reverse('usermodel-list')
        response = self.client.post(url, user_data, format='json')
        # получить пользователя
        url = reverse('usermodel-detail', kwargs={'pk': response.data['id']})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(UserModel.objects.get().first_name, 'Fofo')

    def test_update_account(self):
        """
        Изменить пользователя.
        """
        # создать пользователя
        url = reverse('usermodel-list')
        response = self.client.post(url, user_data, format='json')
        # получить пользователя
        url = reverse('usermodel-detail', kwargs={'pk': response.data['id']})

        new_data = {
            "username": "fofo",
            "first_name": "Fofo",
            "last_name": "Fofo",
            "email": "google@google.com",
            "status": "P",
            "password": "12345678"
        }
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(UserModel.objects.get().email, 'google@google.com')

    def test_delete_account(self):
        """
        Изменить пользователя.
        """
        # создать пользователя
        url = reverse('usermodel-list')
        response = self.client.post(url, user_data, format='json')
        # получить пользователя
        url = reverse('usermodel-detail', kwargs={'pk': response.data['id']})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserModel.objects.count(), 0)
