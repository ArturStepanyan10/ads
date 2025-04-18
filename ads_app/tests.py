from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ads_app.models import Ad, ExchangeProposal


# Тесты для добавления объявления
class AddAdViewTests(TestCase):

    # Установка начальных значений
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.url = reverse('add_ad')

    # Проверка, что доступ к добавлению объявления требует авторизации
    def test_add_ad_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Проверка успешного создания объявления от авторизованного пользователя
    def test_add_ad_creates_ad_with_user(self):
        self.client.login(username='testuser', password='1234')

        data = {
            'title': 'Мой велосипед',
            'description': 'Описание велосипеда',
            'image_url': 'https://avatars.mds.yandex.net/get-mpic/96484/img_id7323107455074381170/orig',
            'category': 'спорт',
            'condition': 'новое',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)
        ad = Ad.objects.first()
        self.assertEqual(ad.user, self.user)

    # Для очистки после каждого теста
    def tearDown(self):
        "Действия после выполнения каждого теста"


# Тесты на действия с предложением обмена (принятие/отклонение)
class OfferActionTests(TestCase):

    # Установка начальных значений
    def setUp(self):
        self.client = Client()

        self.sender = User.objects.create_user(username='sender', password='1234')
        self.receiver = User.objects.create_user(username='receiver', password='1234')

        self.sender_ad = Ad.objects.create(
            user=self.sender,
            title='Старый ноутбук',
            description='Описание старого ноутбука',
            image_url='',
            category='техника',
            condition='хорошее',

        )

        self.receiver_ad = Ad.objects.create(
            user=self.receiver,
            title='Новый телефон',
            description='Описание нового телефона',
            image_url='',
            category='техника',
            condition='новое',

        )

        # Обмен
        self.offer = ExchangeProposal.objects.create(
            ad_sender=self.sender_ad,
            ad_receiver=self.receiver_ad,
            comment='Обмен?'
        )

    # Тест на принятие предложения получателем
    def test_accept_offer_by_receiver(self):
        self.client.login(username='receiver', password='1234')
        url = reverse('offer_action', kwargs={'pk': self.offer.pk})

        response = self.client.post(url, {'action': 'accept'})
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.status, ExchangeProposal.Status.ACCEPTED)

    # Тест на отказ от предложения получателем
    def test_reject_offer_by_receiver(self):
        self.client.login(username='receiver', password='1234')
        url = reverse('offer_action', kwargs={'pk': self.offer.pk})

        response = self.client.post(url, {'action': 'reject'})
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.status, ExchangeProposal.Status.REJECTED)

    # Для очистки после каждого теста
    def tearDown(self):
        "Действия после выполнения каждого теста"


# Тест для редактирования объявлений
class UpdateAdViewTests(TestCase):

    # Установка начальных значений
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test1234')
        self.ad = Ad.objects.create(
            title='Старый мотоблок',
            description='Описание',
            category='Техника',
            condition='б/у',
            user=self.user,
        )

        self.url = reverse('edit_ad', kwargs={'pk': self.ad.pk})

    # Проверка, что пользователь может редактировать свое объявление
    def test_update_own_ad(self):
        self.client.login(username='test', password='test1234')
        response = self.client.get(self.url, {
            'title': 'Старый сломанный мотоблок',
            'description': self.ad.description,
            'image_url': '',
            'category': self.ad.category,
            'condition': self.ad.condition
        })

        self.assertEqual(response.status_code, 200)
        self.ad.refresh_from_db()

    # Проверка, что чужое объявление нельзя редактировать
    def test_cannot_update_foreign_ad(self):
        other_user = User.objects.create_user(username='other', password='54321')
        self.client.login(username='test', password='54321')
        response = self.client.get(self.url, {
            'title': 'Попытка взлома',
            'description': self.ad.description,
            'image_url': '',
            'category': self.ad.category,
            'condition': self.ad.condition
        })
        self.assertEqual(response.status_code, 404)

    # Для очистки после каждого теста
    def tearDown(self):
        "Действия после выполнения каждого теста"


# Тесты для удаления объявления
class DeleteAdViewTests(TestCase):

    # Установка начальных значений
    def setUp(self):
        self.user = User.objects.create_user(username='deleter', password='12345')
        self.ad = Ad.objects.create(
            title='Удаляемое',
            description='Будет удалено',
            category='Разное',
            condition='Состояние',
            user=self.user
        )
        self.url = reverse('delete_ad', kwargs={'pk': self.ad.pk})

    # Проверка, что пользователь может удалить свое объявление
    def test_delete_own_ad(self):
        self.client.login(username='deleter', password='12345')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

    # Проверка, что пользователь не может удалить чужое обьявление
    def test_cannot_delete_foreign_ad(self):
        other_user = User.objects.create_user(username='hacker', password='qwerty')
        self.client.login(username='hacker', password='qwerty')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    # Для очистки после каждого теста
    def tearDown(self):
        "Действия после выполнения каждого теста"


