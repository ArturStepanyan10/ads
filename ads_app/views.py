from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

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

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)


class AddAd(CreateView):
    form_class = AddAdForm
    template_name = 'ads/AddAd.html'
    title_page = 'Создание объявления'
    success_url = reverse_lazy('my_ads')
    extra_context = {
        'title': title_page,
    }

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.user = self.request.user
        return super().form_valid(form)


class UpdateAd(UpdateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/AddAd.html'
    title_page = 'Редактирование объявления'
    success_url = reverse_lazy('my_ads')
    extra_context = {
        'title': title_page,
    }


class DeleteAd(DeleteView):
    model = Ad
    success_url = reverse_lazy("my_ads")

    def get_object(self, queryset=None):
        ad = get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        if ad.user != self.request.user:
            raise Http404("Объявление не найдено")
        return ad



