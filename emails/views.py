from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from concurrent.futures import ThreadPoolExecutor
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from blogs.models import Blog

import logging
logger = logging.getLogger(__name__)

EMAIL_LIST = [
    "test1@example.com",
    "user2@testmail.org",
    "demo3@samplesite.net",
    "trial4@mockdomain.com",
    "sample5@dummymail.co",
]


@staff_member_required
def send_single_email(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)

    if request.method == 'POST':
        try:
            user_email_input = request.POST.get('email')

            if not user_email_input:
                messages.error(request,  'Email address is required')
                return redirect('emails:send_single', slug=slug)

            html_content = render_to_string('emails/blog_email.html', {
                'blog': blog
            })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=blog.title,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email_input]
            )
            email.attach_alternative(html_content, "text/html")

            email.send()

            logger.info(
                f'Single email sent successfully to {user_email_input}')

            messages.success(
                request,  f'Email sent successfully to {user_email_input}')
            return redirect('emails:send_single', slug=slug)

        except Exception as e:
            logger.error(f'Error sending single email: {str(e)}')
            messages.error(
                request,  f'Error : {str(e)}')
            return redirect('emails:send_single', slug=slug)

    return render(request, 'emails/send_single.html')


@staff_member_required
def send_bulk_email(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)

    if request.method == 'POST':
        try:

            html_content = render_to_string('emails/blog_email.html', {
                'blog': blog
            })

            text_content = strip_tags(html_content)

            def send_email_batch(email_batch):
                messages = []
                for email in email_batch:
                    msg = EmailMultiAlternatives(
                        subject=blog.title,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    messages.append(msg)

                try:
                    for msg in messages:
                        msg.send()
                    return len(messages)
                except Exception as e:
                    logger.error(f'Error sending email batch: {str(e)}')
                    messages.error(
                        request, f'Error sending email batch: {str(e)}')
                    return 0

            batch_size = 5
            email_batches = [EMAIL_LIST[i:i + batch_size]
                             for i in range(0, len(EMAIL_LIST), batch_size)]

            total_sent = 0
            failed_emails = []

            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_batch = {executor.submit(
                    send_email_batch, batch): batch for batch in email_batches}

                for future in future_to_batch:
                    try:
                        sent_count = future.result(timeout=30)
                        total_sent += sent_count
                    except Exception as e:
                        failed_batch = future_to_batch[future]
                        failed_emails.extend(failed_batch)
                        logger.error(f'Batch failed: {str(e)}')

            logger.info(
                f'Bulk email completed. Sent: {total_sent}, Failed: {len(failed_emails)}')
            messages.success(
                request,   f'Bulk email completed. Sent: {total_sent}, Failed: {len(failed_emails)}')
            return redirect('emails:send_bulk', slug=slug)

            messages.success(request, {
                'message': f'Bulk email completed successfully',
                'total_sent': total_sent,
                'total_failed': len(failed_emails),
                'failed_emails': failed_emails[:10]
            })
            return redirect('emails:send_bulk', slug=slug)

        except Exception as e:
            logger.error(f'Error in bulk email sending: {str(e)}')
            messages.error(request, f'Error in bulk email sending: {str(e)}')
            return redirect('emails:send_bulk', slug=slug)

    return render(request, 'emails/send_bulk.html', {
        'total_subscribers': len(EMAIL_LIST)
    })
