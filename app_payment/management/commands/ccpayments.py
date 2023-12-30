from django.core.management import BaseCommand

from app_payment.models import Payment
from app_pwl.models import Course, Lesson
from app_users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        payments = [
            {
                'user': users.get(pk=2),
                'course': courses.get(pk=1),
                'lesson': None,
                'payment_amount': 180000,
                'payment_method': 'transfer',
            },
            {
                'user': users.get(pk=3),
                'course': None,
                'lesson': lessons.get(pk=2),
                'payment_amount': 1000,
                'payment_method': 'cash',
            },
            {
                'user': users.get(pk=3),
                'course': courses.get(pk=1),
                'lesson': None,
                'payment_amount': 180000,
                'payment_method': 'transfer',
            },
            {
                'user': users.get(pk=4),
                'course': None,
                'lesson': lessons.get(pk=1),
                'payment_amount': 500,
                'payment_method': 'cash',
            },
            {
                'user': users.get(pk=4),
                'course': courses.get(pk=2),
                'lesson': None,
                'payment_amount': 200000,
                'payment_method': 'cash',
            },

        ]

        for i in payments:
            payment = Payment.objects.create(
                user=i.get('user'),
                course=i.get('course') if i.get('course') else i.get('lesson').course,
                lesson=i.get('lesson'),
                payment_amount=i.get('payment_amount'),
                payment_method=i.get('payment_method'),
            )
            print(payment)
