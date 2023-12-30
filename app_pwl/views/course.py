from django.db.models import Count
from rest_framework import viewsets

from app_payment.services import create_stripe_product, create_stripe_prise
from app_pwl.models import Course
from app_pwl.paginators import CoursePaginator
from app_subscriptions.tasks import curse_update_message
from app_users.permissions import IsModerator, IsOwner
from app_pwl.serializers.course import CourseSerializer, CourseListSerializer, CourseRetrieveSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    default_serializer = CourseSerializer
    serializers = {
        "list": CourseListSerializer,
        "retrieve": CourseRetrieveSerializer,
    }
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        """ Selecting a serializer depending on the request """

        # self.action содержит в себе текущий запрос
        return self.serializers.get(self.action, self.default_serializer)

    def perform_create(self, serializer):
        """ Filling out the "owner" field and creating a course """

        # до создания объекта вызываем проверку на права доступа
        self.check_permissions(self.request)

        new_course = serializer.save()

        if new_course.amount:
            # Создание продукта на сервисе "stripe.com"
            new_course.stripe_product_id = create_stripe_product(new_course.name)
            # Назначение цены продукта на сервисе "stripe.com"
            new_course.stripe_prise_id = create_stripe_prise(new_course)

        new_course.owner = self.request.user
        new_course.save()

    def create(self, request, *args, **kwargs):
        """ Create new course """

        # Можно создавать только авторизованным пользователям не являющимся модераторами
        self.permission_classes = [~IsModerator]
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """ Get course list """

        # При запросе списка курсов
        # в queryset добавляем поле lesson_count
        # путем подсчета объектов привязанных по ForeignKey
        # по related_name поля course модели Lesson
        self.queryset = self.queryset.annotate(lesson_count=Count('lessons'))
        return super().list(request, *args, **kwargs)

        # Просматривать список может любой авторизованный пользователь (заданно в settings)

    def retrieve(self, request, *args, **kwargs):
        """ Get course """

        # Можно просматривать только создателю или модератору
        self.permission_classes = [IsOwner | IsModerator]
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Update course data """

        # Можно изменять только создателю или модератору
        self.permission_classes = [IsOwner | IsModerator]
        curse_update_message.delay(self.get_object().id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Delete course """

        # Можно удалять только создателю
        self.permission_classes = [IsOwner]
        return super().destroy(request, *args, **kwargs)
