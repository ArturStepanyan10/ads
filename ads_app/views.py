from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ads_app.forms import AddAdForm, ExchangeOfferForm, LoginUserForm
from ads_app.models import Ad, ExchangeProposal


class Home(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/index.html'
    title_page = 'Главная страница'
    context_object_name = 'ads'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['search_query'] = self.request.GET.get('q', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['condition_filter'] = self.request.GET.get('condition', '')
        return context

    def get_queryset(self):
        queryset = Ad.objects.exclude(user=self.request.user)
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.order_by('-id')


class MyAds(LoginRequiredMixin, ListView):
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


class AddAd(LoginRequiredMixin, CreateView):
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


class DeleteAd(LoginRequiredMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy("my_ads")

    def get_object(self, queryset=None):
        ad = get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        if ad.user != self.request.user:
            raise Http404("Объявление не найдено")
        return ad


class ExchangeOffer(LoginRequiredMixin, CreateView):
    form_class = ExchangeOfferForm
    template_name = 'ads/ExchangeОffer.html'
    title_page = 'Предложение обмена'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': title_page,
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        ep = form.save(commit=False)
        ad_receiver = get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        ep.ad_receiver = ad_receiver
        return super().form_valid(form)


class ExchangeOfferList(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/ExchangeProposal.html'
    title_page = 'Предложения на обмен'
    context_object_name = 'offers'
    extra_context = {
        'title': title_page,
    }

    def get_queryset(self):
        queryset = ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)

        sender = self.request.GET.get('sender')
        receiver = self.request.GET.get('receiver')
        status = self.request.GET.get('status')

        if sender:
            queryset = queryset.filter(ad_sender__user__username__icontains=sender)
        if receiver:
            queryset = queryset.filter(ad_receiver__user__username__icontains=receiver)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


def offer_action(request, pk):
    if request.method == 'POST':
        offer = get_object_or_404(ExchangeProposal, pk=pk)

        action = request.POST['action']
        if action == 'accept':
            offer.status = offer.Status.ACCEPTED
        elif action == 'reject':
            offer.status = offer.Status.REJECTED
        offer.save()

    return redirect('list_offers')


class MyExchangeProposalsList(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/MyExchangeProposal.html'
    title_page = 'Мои предложения на обмен'
    context_object_name = 'offers'
    extra_context = {
        'title': title_page,
    }

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'ads/Authorization.html'
    extra_context = {
        'title': 'Авторизация'
    }


def logout_view(request):
    logout(request)
    return redirect('login')
