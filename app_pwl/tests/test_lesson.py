from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from app_pwl.models import Lesson, Course
from app_users.models import User


class LessonTest(APITestCase):
    def setUp(self):
        """ Создание необходимых в тестах объектов """

        # Grope "Moderator"
        self.group_moderator = Group.objects.create(name="Moderator")

        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        # Moderator
        self.moderator = User.objects.create(
            email="moderator@test.com",
            is_staff=False,
            is_active=True,
        )
        self.moderator.set_password('test')
        self.moderator.groups.add(self.group_moderator)
        self.moderator.save()

        # Course
        self.course = Course.objects.create(
            name="Test Course",
            description="Description Test Course"
        )

        # Lessons
        self.lesson1 = Lesson.objects.create(
            name="Test Lesson 1",
            description="Description Test Lesson 1",
            course=self.course,
            owner=self.user_1,
        )
        self.lesson2 = Lesson.objects.create(
            name="Test Lesson 2",
            description="Description Test Lesson 2",
            course=self.course,
            owner=self.user_2,
        )

    def test_lesson_create(self):
        """
        Тестирование создания урока обычным пользователем
        с минимальным заполнением полей
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Считаем количество уроков в базе данных
        lesson_count = Lesson.objects.all().count()

        data = {
            "name": "Test Lesson",
            "description": "Description Test Lesson",
            "course": self.course.id,
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

        # Проверяем что в базе данных стало на 1 урок больше
        self.assertEquals(
            Lesson.objects.all().count(),
            lesson_count + 1
        )

    def test_lesson_create_moderator_error(self):
        """ Тестирование ошибки доступа при создании урока модератором """

        # Аутентифицируем модератора
        self.client.force_authenticate(user=self.moderator)

        data = {
            "name": "Test Lesson",
            "description": "Description Test Lesson",
            "course": self.course.id,
        }

        response = self.client.post(
            reverse("app_pwl:lesson_create"),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_create_authenticated_error(self):
        """ Тестирование ошибки доступа при создании урока без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        data = {
            "name": "Test Lesson",
            "description": "Description Test Lesson",
            "course": self.course.id,
        }

        response = self.client.post(
            reverse("app_pwl:lesson_create"),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_list(self):
        """
        Тестирование вывода списка уроков урока
        для любого пользователя и модератора
        """
        for user in [self.user_1, self.user_2, self.moderator]:
            # Аутентифицируемся
            self.client.force_authenticate(user=user)

            response = self.client.get(
                reverse("app_pwl:lesson_list"),
            )

            self.assertEquals(
                response.status_code,
                status.HTTP_200_OK
            )

            self.assertEquals(
                response.json(),
                {
                    'count': 2,
                    'next': None,
                    'previous': None,
                    'results':
                        [
                            {
                                'id': self.lesson1.id,
                                'course': self.course.id,
                                'name': 'Test Lesson 1',
                                'description': 'Description Test Lesson 1'
                            },
                            {
                                'id': self.lesson2.id,
                                'course': self.course.id,
                                'name': 'Test Lesson 2',
                                'description': 'Description Test Lesson 2'
                            }
                        ]
                }
            )

    def test_lesson_list_authenticated_error(self):
        """ Тестирование ошибки доступа при выводе списка уроков без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse("app_pwl:lesson_list"),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_retrieve(self):
        """ Тестирование вывода урока его создателем или модератором"""

        for user in [self.user_1, self.moderator]:
            # Аутентифицируемся
            self.client.force_authenticate(user=user)

            response = self.client.get(
                reverse("app_pwl:lesson_retrieve", kwargs={"pk": self.lesson1.id}),
            )

            self.assertEquals(
                response.status_code,
                status.HTTP_200_OK
            )

            self.assertEquals(
                response.json(),
                {
                    'id': self.lesson1.id,
                    'name': 'Test Lesson 1',
                    'description': 'Description Test Lesson 1',
                    'body': None,
                    'image': None,
                    'video': None,
                    'course': self.course.id,
                    'currency': 'RUB',
                    'amount': 0,
                    'stripe_product_id': None,
                    'stripe_prise_id': None,
                    'owner': self.user_1.id
                }
            )

    def test_lesson_retrieve_owner_error(self):
        """ Тестирование ошибки доступа при выводе урока пользователем не создававшего его """

        # Аутентифицируем пользователя не создававшего урок
        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            reverse("app_pwl:lesson_retrieve", kwargs={"pk": self.lesson1.id}),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_retrieve_authenticated_error(self):
        """ Тестирование ошибки доступа при выводе урока без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse("app_pwl:lesson_retrieve", kwargs={"pk": self.lesson1.id}),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_update_by_owner(self):
        """ Тестирование изменения урока его создателем """

        # Аутентифицируем создателя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "body": "Test updated by user",
        }

        response = self.client.patch(
            reverse("app_pwl:lesson_update", kwargs={"pk": self.lesson1.id}),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {
                'id': self.lesson1.id,
                'name': 'Test Lesson 1',
                'description': 'Description Test Lesson 1',
                'body': 'Test updated by user',
                'image': None,
                'video': None,
                'course': self.course.id,
                'currency': 'RUB',
                'amount': 0,
                'stripe_product_id': None,
                'stripe_prise_id': None,
                'owner': self.user_1.id,
            }
        )

    def test_lesson_update_by_moderator(self):
        """ Тестирование изменения урока модератором """

        # Аутентифицируем создателя
        self.client.force_authenticate(user=self.moderator)

        data = {
            "body": "Test updated by moderator",
        }

        response = self.client.patch(
            reverse("app_pwl:lesson_update", kwargs={"pk": self.lesson1.id}),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {
                'id': self.lesson1.id,
                'name': 'Test Lesson 1',
                'description': 'Description Test Lesson 1',
                'body': 'Test updated by moderator',
                'image': None,
                'video': None,
                'course': self.course.id,
                'currency': 'RUB',
                'amount': 0,
                'stripe_product_id': None,
                'stripe_prise_id': None,
                'owner': self.user_1.id
            }
        )

    def test_lesson_update_owner_error(self):
        """ Тестирование ошибки доступа изменения урока пользователем не создававшем его """

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_2)

        data = {
            "body": "Test updated by moderator",
        }

        response = self.client.patch(
            reverse("app_pwl:lesson_update", kwargs={"pk": self.lesson1.id}),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_update_authenticated_error(self):
        """ Тестирование ошибки доступа изменения урока без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        data = {
            "body": "Test updated by moderator",
        }

        response = self.client.patch(
            reverse("app_pwl:lesson_update", kwargs={"pk": self.lesson1.id}),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_destroy_by_owner(self):
        """ Тестирование удаления урока его создателем """

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Считаем изначальное количество уроков в базе данных
        lesson_count_start = Lesson.objects.all().count()

        # Создаем урок
        create_response = self.client.post(
            reverse("app_pwl:lesson_create"),
            data={
                "name": "Test Lesson",
                "description": "Description Test Lesson",
                "course": self.course.id,
            }
        )

        # Считаем количество уроков в базе данных после создания урока
        lesson_count_created = Lesson.objects.all().count()

        response = self.client.delete(
            reverse("app_pwl:lesson_destroy", kwargs={"pk": create_response.json().get("id")}),
        )

        # Считаем количество уроков в базе данных после удаления урока
        lesson_count_deleted = Lesson.objects.all().count()

        # Проверяем что урок был создан и удален
        self.assertTrue(
            lesson_count_start == (lesson_count_created - lesson_count_deleted) + 1
        )

        # Проверяем ответ, его не должно быть
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_destroy_error(self):
        """ Тестирование удаления урока пользователем не создававшего урок и модератором """

        for user in [self.user_2, self.moderator]:
            # Аутентифицируемся
            self.client.force_authenticate(user=user)

            # Создаем урок от пользователя
            lesson = Lesson.objects.create(
                name="Test Lesson by user_1",
                description="Description Test Lesson by user_1",
                course=self.course,
                owner=self.user_1,
            )

            # Считаем изначальное количество уроков в базе данных
            lesson_count_created = Lesson.objects.all().count()

            response = self.client.delete(
                reverse("app_pwl:lesson_destroy", kwargs={"pk": lesson.id}),
            )

            # Проверяем что урок не был удален
            self.assertTrue(
                Lesson.objects.all().count() == lesson_count_created
            )

            # Проверяем ответ, должна быть ошибка прав доступа
            self.assertEquals(
                response.status_code,
                status.HTTP_403_FORBIDDEN
            )

    def test_lesson_destroy_authenticated_error(self):
        """ Тестирование ошибки доступа при удалении урока без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        # Создаем урок от пользователя
        self.lesson = Lesson.objects.create(
            name="Test Lesson by user_1",
            description="Description Test Lesson by user_1",
            course=self.course,
            owner=self.user_1,
        )

        # Считаем изначальное количество уроков в базе данных до удаления
        lesson_count_created = Lesson.objects.all().count()

        response = self.client.delete(
            reverse("app_pwl:lesson_destroy", kwargs={"pk": self.lesson.id}),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверяем что урок не был удален
        self.assertTrue(
            Lesson.objects.all().count() == lesson_count_created
        )

    def test_lesson_materials_validation(self):
        """
        Тестирование валидации при создании урока,
        с допустимой ссылкой в текстовом поле модели.
        Допускаются только ссылки на youtube.com и email адреса
        """

        # Принудительно аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Текст ограничен 50 символами (согласно максимальной длины для поля "name")
        text_valid_list = [
            "https://www.youtube.com/watch?v=qweasdzxc",
            "www.youtube.com/watch?v=qweasdzxc",
            "youtube.com/watch?v=qweasdzxc",
            "https://youtu.be/qweasdzxc",
            "youtu.be/mHQXz5FctRg",
            "Тест https://www.youtube.com/watch?v=qweasdzxc Ok",
            "Проверка www.youtube.com/watch?v=qweasdzxc link",
            "Проверка youtube.com/watch?v=qweasdzxc link",
            "Проверка https://youtu.be/qweasdzxc link",
            "Проверка youtu.be/mHQXz5FctRg link. qwe/qwe",
            "u_alex90@mail.ru"
            "test@sky.pro"
        ]

        for text in text_valid_list:
            data_list = [
                {
                    "name": text,
                    "description": "Description Test Lesson",
                    "body": "Test text fo test",
                    "course": self.course.id,
                },
                {
                    "name": "Test Lesson",
                    "description": text,
                    "body": "Test text fo test",
                    "course": self.course.id,
                },
                {
                    "name": "Test Lesson",
                    "description": "Description Test Lesson",
                    "body": text,
                    "course": self.course.id,
                },
            ]
            for data in data_list:
                response = self.client.post(
                    reverse("app_pwl:lesson_create"),
                    data=data
                )

                self.assertEquals(
                    response.status_code,
                    status.HTTP_201_CREATED
                )

    def test_lesson_materials_validation_error(self):
        """
        Тестирование валидации при создании урока,
        с НЕдопустимой ссылкой в текстовом поле модели.
        Допускаются только ссылки на youtube.com и email адреса
        """

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user_1)

        # Текст ограничен 50 символами (согласно максимальной длины для поля "name")
        text_invalid_list = [
            "https://dzen.ru/video/watch/qweasdzxc",
            "dzen.ru/video/watch/qweqweqwe",
            "https://vk.com/video-123123123_123123123",
            "vk.com/video-123123123_123123123",
            "Text https://dzen.ru/video/watch/qweasdzxc z. q/w",
            "text dzen.ru/video/watch/qweqweqwe ru, qwe? yu/yu",
            "vid https://vk.com/video-123123123_123123123 go,",
            "nm, vk.com/video-123123123_123123123 jkl",
        ]

        for text in text_invalid_list:
            data_list = [
                {
                    "name": text,
                    "description": "Description Test Lesson",
                    "body": "Test text fo test",
                    "course": self.course.id,
                },
                {
                    "name": "Test Lesson",
                    "description": text,
                    "body": "Test text fo test",
                    "course": self.course.id,
                },
                {
                    "name": "Test Lesson",
                    "description": "Description Test Lesson",
                    "body": text,
                    "course": self.course.id,
                },
            ]
            for data in data_list:
                response = self.client.post(
                    reverse("app_pwl:lesson_create"),
                    data=data
                )

                self.assertEquals(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST
                )
