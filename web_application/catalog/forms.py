from django import forms


class RewiewForm(forms.Form):
    nickname = forms.CharField(max_length=50)
    summary = forms.CharField(max_length=120)
    message = forms.CharField(widget=forms.Textarea)
