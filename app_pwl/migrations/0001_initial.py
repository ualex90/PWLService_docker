# Generated by Django 4.2.7 on 2023-12-04 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('currency', models.CharField(choices=[('RUB', 'Russian ruble'), ('USD', 'USA dollar'), ('EUR', 'Euro')], default='RUB', verbose_name='Currency')),
                ('stripe_product_id', models.CharField(max_length=100, null=True, verbose_name='Stripe product ID')),
                ('stripe_prise_id', models.CharField(max_length=100, null=True, verbose_name='Stripe product ID')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['name', 'description', 'image'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Lesson Materials')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('video', models.CharField(blank=True, max_length=150, null=True, verbose_name='Link to video')),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('currency', models.CharField(choices=[('RUB', 'Russian ruble'), ('USD', 'USA dollar'), ('EUR', 'Euro')], default='RUB', verbose_name='Currency')),
                ('stripe_product_id', models.CharField(max_length=100, null=True, verbose_name='Stripe product ID')),
                ('stripe_prise_id', models.CharField(max_length=100, null=True, verbose_name='Stripe product ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='app_pwl.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ['name', 'description', 'course', 'image', 'video'],
            },
        ),
    ]
