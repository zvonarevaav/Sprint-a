from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class PerevalAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "phone": "1234567890"
        }
        self.coords_data = {
            "latitude": 45.3842,
            "longitude": 7.1525,
            "height": 1200
        }
        self.pereval_data = {
            "beautyTitle": "пер. ",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "coords": self.coords_data,
            "user": self.user_data,
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {"image": "<image_url>", "title": "Седловина"}
            ]
        }

    def test_submit_data(self):
        response = self.client.post('/pereval/submitData/', self.pereval_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())

    def test_get_pereval(self):
        response = self.client.post('/pereval/submitData/', self.pereval_data, format='json')
        pereval_id = response.json()['id']

        response = self.client.get(f'/pereval/submitData/{pereval_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_pereval(self):
        """Проверка метода PATCH /submitData/<id>"""
        # Сначала создаём запись через POST
        response = self.client.post('/pereval/submitData/', self.pereval_data, format='json')
        pereval_id = response.json()['id']

        # Попробуем обновить некоторые данные
        patch_data = {
            "title": "Обновленный перевал",
            "other_titles": "Обновленные названия"
        }

        response = self.client.patch(f'/pereval/submitData/{pereval_id}/edit/', patch_data, format='json')

        print(f"Ответ сервера PATCH: {response.json()}")  # Логируем ответ сервера для отладки

        # Проверка что сервер вернул state = 1
        self.assertEqual(response.json()['state'], 1)  # Проверка на успешное обновление
        self.assertEqual(response.status_code, status.HTTP_200_OK)

