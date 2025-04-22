from django import forms
from .models import MentorshipContact, ExpertiseContact, ResumeReviewContact


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
