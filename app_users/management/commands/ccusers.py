from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        group_moderator = Group.objects.create(name="Moderator")

        users = [
            {
                'email': 'ivanov@sky.pro',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'is_staff': False,
                'is_active': True,
                'password': '123qwe',
                'is_moderator': True,
            },
            {
                'email': 'petrov@sky.pro',
                'first_name': 'Петр',
                'last_name': 'Петров',
                'is_staff': False,
                'is_active': True,
                'password': '123qwe',
                'is_moderator': False,
            },
            {
                'email': 'sidorov@sky.pro',
                'first_name': 'Сидор',
                'last_name': 'Сидоров',
                'is_staff': False,
                'is_active': True,
                'password': '123qwe',
                'is_moderator': False,
            },
        ]
        count = 0
        for i in users:
            user = User.objects.create(
                email=i.get('email'),
                first_name=i.get('first_name'),
                last_name=i.get('last_name'),
                is_staff=i.get('is_staff'),
                is_active=i.get('is_active'),
            )
            user.set_password(i.get('password'))

            if i.get('is_moderator'):
                user.groups.add(group_moderator)

            user.save()
            count += 1

            print(f'{count}. email: {user.email}, password: {i.get("password")}'
                  f'{"; MODERATOR" if i.get("is_moderator") else ""};')
