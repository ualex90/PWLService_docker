
from django.core.management import BaseCommand

from app_users.tasks import user_login_per_month


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_login_per_month()
