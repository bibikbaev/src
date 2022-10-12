from django import forms
from django_starfield import Stars as Starfield
from .models import *
from django.contrib.auth.models import User
SCORE_CHOICES = [
    ('rating-5', ''),
    ('rating-4', ''),
    ('rating-3', ''),
    ('rating-2', ''),
    ('rating-1', '')
    ]


class StarsForm(forms.Form):
    rating = forms.CharField(widget=forms.RadioSelect(choices=SCORE_CHOICES))


class MessageForm(forms.Form):
    review_text = forms.CharField(label='Комментарий', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'message', 'id': 'message', 'rows': '7', 'cols': '30', 'placeholder':'Сообщение (можно написать кратко)'}))
    contact_info = forms.CharField(label='Номер телефона, telegram, ВК и тд', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'contact', 'id': 'contact', 'placeholder':'Номер или другие контакты (по желанию)'}))
    name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'name', 'id': 'name', 'placeholder':'Имя (по желанию)'}))


class ProfileUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-line'}))

    class Meta(object):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-line'})
