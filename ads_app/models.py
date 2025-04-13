from django.contrib.auth.models import User
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image_url = models.URLField(verbose_name='Адрес фото', blank=True, null=True)
    category = models.CharField(max_length=100, verbose_name='Категория')
    condition = models.CharField(max_length=100, verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class ExchangeProposal(models.Model):
    class Status(models.TextChoices):
        AWAITING = 'ОЖИДАЕТ'
        ACCEPTED = 'ПРИНЯТА'
        REJECTED = 'ОТКЛОНЕНА'

    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.AWAITING,
                              verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE,
                                  verbose_name='Объявление отправителя')
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE,
                                    verbose_name='Объявление получателя')

    def __str__(self):
        return f"{self.ad_sender.user} : {self.ad_receiver.user} {self.status}"

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        ordering = ['-created_at']
