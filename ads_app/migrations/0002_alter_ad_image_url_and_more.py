# Generated by Django 5.2 on 2025-04-13 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='Адрес фото'),
        ),
        migrations.AlterField(
            model_name='exchangeproposal',
            name='ad_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='ads_app.ad', verbose_name='Объявление получателя'),
        ),
        migrations.AlterField(
            model_name='exchangeproposal',
            name='ad_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='ads_app.ad', verbose_name='Объявление отправителя'),
        ),
    ]
