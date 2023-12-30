from django.db import models
from django.utils.translation import gettext_lazy as _

from app_pwl.models import Course
from app_users.models import NULLABLE
from config import settings


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Subscriber'),
        related_name="courses",
        **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        verbose_name=_('Course'),
        related_name="subscribers",
    )
