from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        email = 'admin@sky.pro'
        password = 'admin'

        user = User.objects.create(
            email=email,
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password(password)
        user.save()
        print(f'email: {email}\npassword: {password}')
