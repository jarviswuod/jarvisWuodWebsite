from django import forms
from .models import BookCall, MentorshipContact, ExpertiseContact, ResumeReviewContact, NewsletterSubscriber


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


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'
        # widgets = {
        #     'email_address': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'bg-white text-black text-base w-full sm:w-2/3 p-4 border border-gray-300 rounded'})
        # }

    # def clean_email(self):
    #     email_address = self.cleaned_data.get('email_address')
    #     if NewsletterSubscriber.objects.filter(email_address=email_address).exists():
    #         raise forms.ValidationError("This email is already subscribed.")
    #     return email_address
