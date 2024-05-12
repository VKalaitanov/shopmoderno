from django import forms
from django.core.exceptions import ValidationError

from .models import Review, Feedback


class ReviewForm(forms.ModelForm):
    user = forms.HiddenInput()
    review = forms.CharField(
        max_length=1000,
        label='Добавить отзыв:',
        widget=forms.Textarea(attrs={'class': 'form-area'})
    )

    def clean_review(self):
        review = self.cleaned_data['review']
        if len(review) > 1000:
            raise ValidationError('Длина превышает 1000 символов')

        return review

    class Meta:
        model = Review
        fields = ('review', 'rating')


class FeedbackCreateForm(forms.ModelForm):
    """
    Форма отправки обратной связи
    """
    # subject = forms.CharField(label='',max_length=100, widget=forms.Textarea(attrs={'placeholder': 'form-input'}))

    class Meta:
        model = Feedback
        fields = ('subject', 'email', 'content')
        labels = {
            'subject': '',
            'email': '',
            'content': '',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Тема письма'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Электронный адрес (email)'}),
            'content': forms.Textarea(attrs={'placeholder': 'Содержимое письма'}),
        }


