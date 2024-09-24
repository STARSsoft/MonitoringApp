from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm



class UserRegistrationForm(forms.ModelForm):    # Форма регистрации пользователя
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email



class UserProfileForm(forms.ModelForm): # Форма личного кабинета пользователя
    email = forms.EmailField(label=_("Email address"))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Email обязательно для заполнения


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=None  # Убираем подсказки по умолчанию
    )

    new_password2 = forms.CharField(
        label=_("Подтвердите новый пароль"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=None  # Убираем подсказки по умолчанию
    )

