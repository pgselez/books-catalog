from django import forms
from .models import Review


class ReviewForm(forms.Form):
    nickname = forms.CharField(max_length=50)
    summary = forms.CharField(max_length=120)
    message = forms.CharField(widget=forms.Textarea)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=255)


class ModelReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['nickname', 'summary', 'review']
