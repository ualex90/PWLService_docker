# Generated by Django 4.2.8 on 2023-12-07 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_subscriptions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='Subscriber'),
            preserve_default=False,
        ),
    ]
