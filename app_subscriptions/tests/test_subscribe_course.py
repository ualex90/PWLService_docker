from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_pwl.models import Course
from app_subscriptions.models import Subscription
from app_users.models import User


class SubscriptionTest(APITestCase):
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

        # Courses
        self.course_1 = Course.objects.create(
            name="Test Course_1",
            description="Description Test Course_1",
            owner=self.user_1
        )
        self.course_2 = Course.objects.create(
            name="Test Course_2",
            description="Description Test Course_2",
            owner=self.user_1
        )

    def test_subscribe_course(self):
        """ Тестирование создания подписки обычным пользователем """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Считаем количество подписок в базе данных
        subscribe_count = Subscription.objects.all().count()

        response = self.client.post(
            reverse("app_subscriptions:subscribe_course"),
            data={
                "course": self.course_1.id
            }
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что в базе данных стало на 1 урок больше
        self.assertTrue(
            Subscription.objects.all().count() == subscribe_count + 1
        )

    def test_subscribe_course_duplicate(self):
        """ Тестирование невозможности сохранения дубликата подписки """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Считаем количество подписок в базе данных до их создания
        subscribe_count = Subscription.objects.all().count()

        # Создаем подписку
        response = self.client.post(
            reverse("app_subscriptions:subscribe_course"),
            data={
                "course": self.course_1.id
            }
        )

        # Создаем дубликат подписки
        response_duplicate = self.client.post(
            reverse("app_subscriptions:subscribe_course"),
            data={
                "course": self.course_1.id
            }
        )

        # Проверяем что подписка успешно создана
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что при попытке создания дубликата подписки не вызываются ошибки,
        # Должен приходить ответ что как буд-то подписка создана (она ведь и так существует)
        self.assertEquals(
            response_duplicate.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что в базе данных стало только на 1 урок больше
        self.assertTrue(
            Subscription.objects.all().count() == subscribe_count + 1
        )

    def test_subscribe_course_moderator_error(self):
        """ Тестирование ошибки доступа создания подписки модератором """

        # Аутентифицируем модератора
        self.client.force_authenticate(user=self.moderator)

        # Считаем количество подписок в базе данных до создания
        subscribe_count = Subscription.objects.all().count()

        response = self.client.post(
            reverse("app_subscriptions:subscribe_course"),
            data={
                "course": self.course_1.id
            }
        )

        # Проверяем что вернулась ошибка доступа
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверяем что в базе данных количество подписок не изменилось
        self.assertEquals(
            Subscription.objects.all().count(),
            subscribe_count
        )

    def test_subscribe_course_authenticated_error(self):
        """ Тестирование ошибки доступа создания подписки без аутентификации """

        # Выходим из системы
        self.client.force_authenticate(user=None)

        # Считаем количество подписок в базе данных до создания
        subscribe_count = Subscription.objects.all().count()

        response = self.client.post(
            reverse("app_subscriptions:subscribe_course"),
            data={
                "course": self.course_1.id
            }
        )

        # Проверяем что вернулась ошибка доступа
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверяем что в базе данных количество подписок не изменилось
        self.assertTrue(
            Subscription.objects.all().count() == subscribe_count
        )

    def test_unsubscribe_course(self):
        """
        Тестирование удаления подписки пользователем
        создавшим ее
        """

        # Создаем подписку от имени user_1
        subscription = Subscription.objects.create(
            user=self.user_1,
            course=self.course_1,
        )

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Считаем количество подписок в базе данных
        subscription_count = Subscription.objects.all().count()

        response = self.client.delete(
            reverse("app_subscriptions:unsubscribe_course", kwargs={"pk": subscription.id})
        )

        # Проверяем ответ, его не должно быть
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Проверяем что подписка удалена
        self.assertTrue(
            Subscription.objects.all().count() == subscription_count - 1
        )

    def test_unsubscribe_course_moderator_error(self):
        """
        Тестирование ошибки доступа при удалении подписки
        пользователем не создававшего ее или модератором
        """

        # Создаем подписку от имени user_1
        subscription = Subscription.objects.create(
            user=self.user_1,
            course=self.course_1,
        )

        for user in [self.user_2, self.moderator]:
            # Аутентифицируемся
            self.client.force_authenticate(user=user)

            # Считаем количество подписок в базе данных
            subscription_count = Subscription.objects.all().count()

            response = self.client.delete(
                reverse("app_subscriptions:unsubscribe_course", kwargs={"pk": subscription.id})
            )

            # Проверяем ответ, должна быть ошибка доступа
            self.assertEquals(
                response.status_code,
                status.HTTP_403_FORBIDDEN
            )

            # Проверяем что количество подписок не изменилось
            self.assertTrue(
                Subscription.objects.all().count() == subscription_count
            )

    def test_unsubscribe_course_authenticated_error(self):
        """
        Тестирование ошибки доступа при удалении подписки
        без аутентификации
        """

        # Создаем подписку от имени user_1
        subscription = Subscription.objects.create(
            user=self.user_1,
            course=self.course_1,
        )

        # Выходим из системы
        self.client.force_authenticate(user=None)

        # Считаем количество подписок в базе данных
        subscription_count = Subscription.objects.all().count()

        response = self.client.delete(
            reverse("app_subscriptions:unsubscribe_course", kwargs={"pk": subscription.id})
        )

        # Проверяем ответ, должна быть ошибка аутентификации
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверяем что количество подписок не изменилось
        self.assertTrue(
            Subscription.objects.all().count() == subscription_count
        )

    def test_subscriptions_in_course_list(self):
        """ Тестирование наличия информации о подписанных пользователях в экземпляре course """

        # Создадим дополнительный курс
        course_3 = Course.objects.create(
            name="Test Course_3",
            description="Description Test Course_3",
            owner=self.user_2
        )

        # Создаем подписку от имени user_2 на course_2
        subscription = Subscription.objects.create(
            user=self.user_2,
            course=self.course_2,
        )

        # Аутентифицируем user_2
        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            '/course/',
        )

        # Проверяем что пользователь user_2 подписан только на курс course_2
        self.assertEquals(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.course_1.id,
                        'lesson_count': 0,
                        'is_subscribe': False,
                        'name': 'Test Course_1',
                        'description': 'Description Test Course_1',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_1.id
                    },
                    {
                        'id': self.course_2.id,
                        'lesson_count': 0,
                        'is_subscribe': True,
                        'name': 'Test Course_2',
                        'description': 'Description Test Course_2',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_1.id
                    },
                    {
                        'id': course_3.id,
                        'lesson_count': 0,
                        'is_subscribe': False,
                        'name': 'Test Course_3',
                        'description': 'Description Test Course_3',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_2.id
                    }
                ]
            }
        )

        # Аутентифицируем user_1
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            '/course/',
        )

        # Проверяем что пользователь user_1 не подписан ни на один курс
        self.assertEquals(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.course_1.id,
                        'lesson_count': 0,
                        'is_subscribe': False,
                        'name': 'Test Course_1',
                        'description': 'Description Test Course_1',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_1.id
                    },
                    {
                        'id': self.course_2.id,
                        'lesson_count': 0,
                        'is_subscribe': False,
                        'name': 'Test Course_2',
                        'description': 'Description Test Course_2',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_1.id
                    },
                    {
                        'id': course_3.id,
                        'lesson_count': 0,
                        'is_subscribe': False,
                        'name': 'Test Course_3',
                        'description': 'Description Test Course_3',
                        'image': None,
                        'currency': 'RUB',
                        'amount': 0,
                        'stripe_product_id': None,
                        'stripe_prise_id': None,
                        'owner': self.user_2.id
                    }
                ]
            }
        )
