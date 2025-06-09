from django import forms
from .models import Newsletter, Subscriber, UnsubscribeFeedback


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'subject', 'content', 'html_content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Newsletter title'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email subject line'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 10,
                'placeholder': 'Plain text content'
            }),
            'html_content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 15,
                'placeholder': 'HTML content (optional)'
            }),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            existing = Subscriber.objects.get(email=email)
            self.instance = existing
        return email


class UnsubscribeFeedbackForm(forms.ModelForm):
    class Meta:
        model = UnsubscribeFeedback
        fields = ['primary_reason', 'additional_feedback', 'would_resubscribe']
        widgets = {
            'primary_reason': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'additional_feedback': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Please share any additional feedback (optional)'
            }),
            'would_resubscribe': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
        }
        labels = {
            'primary_reason': 'What\'s the main reason for unsubscribing?',
            'additional_feedback': 'Additional feedback',
            'would_resubscribe': 'I might resubscribe in the future if content improves',
        }
