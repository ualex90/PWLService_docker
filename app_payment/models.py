from django.db import models
from django.utils.translation import gettext_lazy as _

from app_pwl.models import Course, Lesson
from app_users.models import User, NULLABLE


class Payment(models.Model):

    # Choices для способа оплаты
    class PymentMethodChoice(models.TextChoices):
        TRANSFER = 'transfer', _('Transfer')
        USD = 'cash', _('Cash')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='payments'
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Payment date")
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Paid course"),
        **NULLABLE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name=_("Paid lesson"),
        **NULLABLE
    )

    payment_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Payment amount")
    )

    payment_method = models.CharField(
        default=PymentMethodChoice.TRANSFER,
        max_length=8,
        choices=PymentMethodChoice.choices,
        verbose_name=_("Payment Method")
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        purpose = f"Курс: {self.course.name}" if self.course else (f"Курс: {self.lesson.course.name}\n"
                                                                   f"Урок: {self.lesson.name}")
        return f'{self.user}\n{self.date}\n{purpose}\n'


class StripeSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='payment_sessions',
        **NULLABLE
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Create date")
    )

    payment_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Payment amount"),
        **NULLABLE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course for payment"),
        **NULLABLE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name=_("Lesson for payment"),
        **NULLABLE
    )

    session_url = models.CharField(
        max_length=400,
        verbose_name=_("Session URL"),
        **NULLABLE
    )
