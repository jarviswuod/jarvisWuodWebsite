from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from blogs.models import Blog

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
                messages.error(request, 'Email address is required')
                return redirect('emails:send_single', slug=slug)

            html_content = render_to_string('emails/blog_email.html', {
                'blog': blog
            })

            text_content = strip_tags(html_content)

            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=user_email_input,
                subject=blog.title,
                html_content=html_content,
                plain_text_content=text_content
            )

            try:
                sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
                response = sg.send(message)
                logger.info(f"Email sent! Status code: {response.status_code}")
            except Exception as sendgrid_error:
                logger.error(f"SendGrid error: {sendgrid_error}")

            logger.info(
                f'Single email sent successfully to {user_email_input}')
            return redirect('emails:send_single', slug=slug)

        except Exception as e:
            logger.error(f'Error sending single email: {str(e)}')
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
                sent_count = 0
                for email in email_batch:
                    message = Mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to_emails=email,
                        subject=blog.title,
                        html_content=html_content,
                        plain_text_content=text_content
                    )

                    try:
                        sg = SendGridAPIClient(
                            api_key=settings.SENDGRID_API_KEY)
                        response = sg.send(message)
                        logger.info(
                            f"Email sent to {email}! Status code: {response.status_code}")
                        sent_count += 1
                    except Exception as sendgrid_error:
                        logger.error(
                            f"SendGrid error for {email}: {sendgrid_error}")

                return sent_count

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

            logger.info({'message': f'Bulk email completed successfully', 'total_sent': total_sent,
                        'total_failed': len(failed_emails), 'failed_emails': failed_emails[:10]})
            return redirect('emails:send_bulk', slug=slug)

        except Exception as e:
            logger.error(f'Error in bulk email sending: {str(e)}')
            return redirect('emails:send_bulk', slug=slug)

    return render(request, 'emails/send_bulk.html', {
        'total_subscribers': len(EMAIL_LIST)
    })
