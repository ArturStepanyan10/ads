from django import forms
from django.core.exceptions import ValidationError

from ads_app.models import Ad, ExchangeProposal


class AddAdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 70:
            raise ValidationError("Длина превышает 50 символов")

        return title


class ExchangeOfferForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)



