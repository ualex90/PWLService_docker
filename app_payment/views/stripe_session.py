from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_payment.serializers.stripe_session import StripeSessionSerializer
from app_payment.services import create_stripe_session
from app_pwl.models import Lesson, Course
from app_users.permissions import IsModerator


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Create payment session """

    serializer_class = StripeSessionSerializer

    # Покупать можно только авторизованным пользователям не являющимся модераторами
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_session = serializer.save()

        # Присвоение пользователя
        new_session.user = self.request.user

        # Заполнение полей в зависимости от выбора (урок или курс)
        if course_id := self.request.data.get('course'):
            course = Course.objects.get(pk=course_id)
            new_session.payment_amount = course.amount
            new_session.session_url = create_stripe_session(course.stripe_prise_id)
        elif lesson_id := self.request.data.get('lesson'):
            lesson = Lesson.objects.get(pk=lesson_id)
            new_session.payment_amount = lesson.amount
            new_session.session_url = create_stripe_session(lesson.stripe_prise_id)

        new_session.save()
