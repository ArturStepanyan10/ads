from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from ads_app.forms import AddAdForm
from ads_app.models import Ad


class Home(ListView):
    model = Ad
    template_name = 'ads/index.html'
    title_page = 'Главная страница'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Ad.objects.all()


class MyAds(ListView):
    model = Ad
    template_name = 'ads/myAds.html'
    title_page = 'Мои объявления'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context


class AddAd(CreateView):
    form_class = AddAdForm
    template_name = 'ads/AddAd.html'
    title_page = 'Добавление объявления'
    success_url = reverse_lazy('my_ads')

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        return super().form_valid(form)

