# Generated by Django 5.2 on 2025-04-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0002_alter_ad_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangeproposal',
            name='status',
            field=models.CharField(choices=[('Ожидает', 'ОЖИДАЕТ'), ('Принята', 'ПРИНЯТА'), ('Отклонена', 'ОТКЛОНЕНА')], default='Ожидает', max_length=50, verbose_name='Статус'),
        ),
    ]
