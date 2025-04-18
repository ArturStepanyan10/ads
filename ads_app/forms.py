from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from ads_app.models import Ad, ExchangeProposal


# Форма добавления объявлений
class AddAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 70:
            raise ValidationError("Длина превышает 70 символов")

        return title


# Форма предложений
class ExchangeOfferForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)


# Форма авторизации
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
