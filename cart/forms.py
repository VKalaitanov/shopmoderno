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
        queryset=Size.objects.none(),
        empty_label='',
        label='Размер',
    )

    class Meta:
        model = ProductSize
        fields = ('quantity', 'size')

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            self.fields['size'].queryset = Size.objects.filter(
                sizes__product_id=product_id, sizes__quantity__gt=0
            ).distinct()


