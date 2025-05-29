from django.shortcuts import render, redirect
# from django.core.mail import send_mail

# from django.contrib import messages


def blogs(request):
    context = {}
#     form = NewsletterForm()
#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)

#         if form.is_valid():
#             email_address = form.cleaned_data['email_address']

#             # Save subscriber to database
#             subscriber = form.save()

#             # Send confirmation email
#             subject = "Welcome to Jarvis Wuod's Newsletter"
#             message = f"""
#             Hi there,

#             Thank you for subscribing to my newsletter.

#             You'll receive thoughtful content straight to your inbox.
#             No spam, just valuable insights.

#             If you ever want to unsubscribe, simply click the unsubscribe link at the bottom of any newsletter email.

#             Best regards,
#             Jarvis Wuod
#             """
#             # from_email = settings.DEFAULT_FROM_EMAIL
#             # recipient_list = [email_address]

#             try:
#                 # send_mail(subject, message, 'your@email.com',
#                 #           [email_address], fail_silently=False)
#                 send_confirmation_email_celery.delay(
#                     subject='Your Call Booking Confirmation',
#                     message='Thank you for booking a call...',
#                     from_email='jarviswuod@gmail.com',
#                     recipient_list=[email_address]
#                 )
#                 messages.success(request, "You have successfully subscribed!")
#             except Exception as e:

#                 messages.warning(
#                     request, "Subscription successful, but there was an issue sending the confirmation email.")

#             return redirect('blogs')
#         else:
#             messages.error(
#                 request, "There was an error with your submission. Please check the form and try again.")

#     context = {'form': form}

    return render(request, 'blogs/blogs.html', context)
