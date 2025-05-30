from django import forms
from .models import BookCall, MentorshipContact, ExpertiseContact, ResumeReviewContact


class BookCallForm(forms.ModelForm):
    class Meta:
        model = BookCall
        fields = '__all__'


class MentorshipForm(forms.ModelForm):
    class Meta:
        model = MentorshipContact
        fields = '__all__'


class ExpertiseForm(forms.ModelForm):
    class Meta:
        model = ExpertiseContact
        fields = '__all__'


class ResumeReviewForm(forms.ModelForm):
    class Meta:
        model = ResumeReviewContact
        fields = '__all__'
