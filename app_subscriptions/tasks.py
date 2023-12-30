import smtplib

from celery import shared_task
from django.core.mail import send_mass_mail

from app_pwl.models import Course
from app_subscriptions.models import Subscription
from config.settings import EMAIL_HOST


@shared_task
def curse_update_message(course_id, message=None):
    course = Course.objects.get(pk=course_id)
    if not message:
        message = f"Обновлен курс {course.name}"
    # формирование сообщений
    message_list = get_message_list(course, message)

    # Отправка сообщений
    if message_list:
        try:
            send_mass_mail(message_list, fail_silently=False)
        except smtplib.SMTPSenderRefused:
            server_response = 'Адрес отправителя отклонен: он не принадлежит авторизующемуся пользователю'
        except smtplib.SMTPAuthenticationError:
            server_response = 'Ошибка авторизации. Неправильное имя пользователя или пароль'
        except OSError:
            server_response = f'Хост ({EMAIL_HOST}) недоступен'
        else:
            server_response = (f'Сообщение о обновлении курса "{course.name}" '
                               f'успешно отправлено {len(message_list)} пользователям')

        print(server_response)
        return server_response


def get_message_list(course, message):
    message_list = []
    for subscription in Subscription.objects.filter(course=course):
        body = (f'Привет {subscription.user.first_name}!\n'
                f'{message} \n\n'
                f'Данное сообщение сформировано автоматически. Просьба не отвечать.')
        message = (f"Обновление на курсе {course.name}",
                   body,
                   None,
                   [subscription.user.email])
        message_list.append(message)

    return message_list
