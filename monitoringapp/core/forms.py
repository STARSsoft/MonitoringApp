# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from .models import Price, Product, Region, UnitOfMeasurement



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



class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['ID_region', 'ID_product', 'ID_measure', 'quantity', 'price']
        labels = {
            'ID_region': _('Регион'),
            'ID_product': _('Продукт'),
            'ID_measure': _('Единица измерения'),
            'quantity': _('Количество'),
            'price': _('Цена'),
        }

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'ru')
        super().__init__(*args, **kwargs)

        # Динамическое обновление наименований полей в зависимости от языка
        if language == 'kk':
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_KZ
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_KZ
        elif language == 'en':
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_EN
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_EN
        else:
            self.fields['ID_product'].queryset = Product.objects.all()
            self.fields['ID_product'].label_from_instance = lambda obj: obj.product_RU
            self.fields['ID_region'].queryset = Region.objects.all()
            self.fields['ID_region'].label_from_instance = lambda obj: obj.region_RU

        # Изначально оставляем поле с единицей измерения пустым, так как оно будет загружаться динамически
        self.fields['ID_measure'].queryset = UnitOfMeasurement.objects.none()
