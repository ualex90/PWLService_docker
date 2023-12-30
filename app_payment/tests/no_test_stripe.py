from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_pwl.models import Course, Lesson
from app_users.models import User


class StripeTest(APITestCase):
    def setUp(self):
        """ Создание необходимых в тестах объектов """

        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        # Course
        self.course_1 = Course.objects.create(
            name="Test Course",
            description="Description Test Course"
        )

    def test_lesson_create(self):
        """
        Тестирование создания урока на "stripe.com"
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "name": "Test Lesson",
            "description": "Description Test Lesson",
            "course": self.course_1.id,
            "amount": 250
        }

        response = self.client.post(
            reverse("app_pwl:lesson_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что поле stripe_prise_id созданного объекта не None
        self.assertTrue(
            Lesson.objects.get(pk=response.json().get('id')).stripe_prise_id
        )

    def test_course_create(self):
        """
        Тестирование создания курса на "stripe.com"
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "name": "Test Course",
            "description": "Description Test Course",
            "amount": 2500
        }

        response = self.client.post(
            "/course/",
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что поле stripe_prise_id созданного объекта не None
        self.assertTrue(
            Course.objects.get(pk=response.json().get('id')).stripe_prise_id
        )
