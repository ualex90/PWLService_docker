from datetime import timedelta, datetime

from app_users.models import User


def user_login_per_month():
    now = datetime.now()
    invalid_date = now - timedelta(days=30)
    print(invalid_date)
    users_invalid = User.objects.filter(last_login__lt=invalid_date)
    print(users_invalid)
    for user in users_invalid:
        user.is_active = False
