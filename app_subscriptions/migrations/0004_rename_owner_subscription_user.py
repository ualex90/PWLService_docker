# Generated by Django 4.2.8 on 2023-12-07 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_subscriptions', '0003_alter_subscription_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='owner',
            new_name='user',
        ),
    ]
