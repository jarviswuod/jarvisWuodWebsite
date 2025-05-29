from django import forms
from .models import BookCall


class BookCallForm(forms.ModelForm):
    class Meta:
        model = BookCall
        fields = '__all__'
