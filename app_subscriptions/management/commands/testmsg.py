from django.core.management import BaseCommand

from app_pwl.models import Course
from app_subscriptions.tasks import curse_update_message


class Command(BaseCommand):

    def handle(self, *args, **options):
        curse_update_message(Course.objects.get(pk=1))
