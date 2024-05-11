from django import forms
from moderno.models import ProductSize, Size


class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        label='Количество',
        initial=1
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        empty_label='',
        label='Размер',
    )

    class Meta:
        model = ProductSize
        fields = ('quantity', 'size')
