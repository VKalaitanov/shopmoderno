import re

from django import forms
from django.core.exceptions import ValidationError

from order.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'postal_code', 'city')

        labels = {
            'first_name': '',
            'last_name': '',
            'phone': '',
            'address': '',
            'postal_code': '',
            'city': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Почтовый индекс'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        cleaned_phone_number = re.sub(r'\D', '', phone)

        if not re.match(r'^7\d{10}$', cleaned_phone_number):
            raise ValidationError('Неверный формат номера телефона')

        return cleaned_phone_number
