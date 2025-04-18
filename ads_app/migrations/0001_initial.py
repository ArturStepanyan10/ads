# Generated by Django 5.2 on 2025-04-13 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image_url', models.URLField(verbose_name='Адрес фото')),
                ('category', models.CharField(max_length=100, verbose_name='Категория')),
                ('condition', models.CharField(max_length=100, verbose_name='Состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExchangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('ОЖИДАЕТ', 'Awaiting'), ('ПРИНЯТА', 'Accepted'), ('ОТКЛОНЕНА', 'Rejected')], default='ОЖИДАЕТ', max_length=50, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('ad_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='ads_app.ad', verbose_name='Получатель')),
                ('ad_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='ads_app.ad', verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Предложение обмена',
                'verbose_name_plural': 'Предложения обмена',
                'ordering': ['-created_at'],
            },
        ),
    ]
