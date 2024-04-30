from django import forms
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    user = forms.HiddenInput()
    review = forms.CharField(
        max_length=1000,
        label='Добавить комментарий:',
        widget=forms.Textarea(attrs={'class': 'form-area'})
    )

    def clean_review(self):
        review = self.cleaned_data['review']
        if len(review) > 1000:
            raise ValidationError("Длина превышает 1000 символов")

        return review

    class Meta:
        model = Review
        fields = ('review', 'rating')
