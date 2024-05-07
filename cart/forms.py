# from django import forms
#
# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
#
#
# class CartAddProductForm(forms.Form):
#     quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
#     update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

from django import forms
from django.db.models import Sum

from moderno.models import Product, ProductSize, Size


class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        label='Количество товара',
        # widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        empty_label='Выберите размер',
        label='Размер',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = ProductSize
        fields = ('quantity', 'size')

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if type(quantity) == str:
            raise forms.ValidationError('Введите число')
        return quantity
