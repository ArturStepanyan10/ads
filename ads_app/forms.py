from django import forms
from django.core.exceptions import ValidationError

from ads_app.models import Ad


class AddAdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title
