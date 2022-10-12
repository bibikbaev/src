from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class ProfileUserForm(AuthenticationForm):
    class Meta(object):
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"

