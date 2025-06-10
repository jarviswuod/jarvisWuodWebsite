
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from blogs.models import Blog

logger = logging.getLogger(__name__)

EMAIL_LIST = [
    'jarviswuod@gmail.com',
    'jarvis@afrisoltech.co.ke',
    'jarvisochieng2018@gmail.com',
]


def send_single_email(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)

    """
    Send a single blog email with HTML template
    """
    if request.method == 'POST':
        try:

            data = json.loads(
                request.body) if request.content_type == 'application/json' else request.POST

            recipient_email = data.get('email')
            blog_title = data.get('title', 'Latest Blog Post')
            blog_content = data.get('content', '')

            if not recipient_email:
                return JsonResponse({'error': 'Email address is required'}, status=400)

            html_content = render_to_string('emails/blog_email.html', {
                'blog': blog,
                'blog_title': blog.title,
                'recipient_email': recipient_email,
            })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=blog.title,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email]
            )
            email.attach_alternative(html_content, "text/html")

            email.send()

            logger.info(f'Single email sent successfully to {recipient_email}')
            return JsonResponse({
                'success': True,
                'message': f'Email sent successfully to {recipient_email}'
            })

        except Exception as e:
            logger.error(f'Error sending single email: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'emails/send_single.html')


def send_bulk_email(request):
    """
    Send bulk emails to all subscribers with optimizations
    Uses threading and batching for better performance
    """
    if request.method == 'POST':
        try:
            # Get data from request
            data = json.loads(
                request.body) if request.content_type == 'application/json' else request.POST

            blog_title = data.get('title', 'Latest Blog Post')
            blog_content = data.get('content', '')
            blog_url = data.get('url', '#')
            author_name = data.get('author', 'Blog Author')

            # Render HTML email template once
            html_content = render_to_string('emails/blog_email.html', {
                'blog_title': blog_title,
                'blog_content': blog_content,
                'blog_url': blog_url,
                'author_name': author_name,
            })

            # Create plain text version
            text_content = strip_tags(html_content)

            # Optimization 1: Batch processing
            def send_email_batch(email_batch):
                """Send emails in batches to avoid overwhelming the server"""
                messages = []
                for email in email_batch:
                    msg = EmailMultiAlternatives(
                        subject=f'New Blog Post: {blog_title}',
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    messages.append(msg)

                # Send batch
                try:
                    for msg in messages:
                        msg.send()
                    return len(messages)
                except Exception as e:
                    logger.error(f'Error sending email batch: {str(e)}')
                    return 0

            # Optimization 2: Split emails into batches of 10
            batch_size = 10
            email_batches = [EMAIL_LIST[i:i + batch_size]
                             for i in range(0, len(EMAIL_LIST), batch_size)]

            total_sent = 0
            failed_emails = []

            # Optimization 3: Use ThreadPoolExecutor for concurrent sending
            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_batch = {executor.submit(
                    send_email_batch, batch): batch for batch in email_batches}

                for future in future_to_batch:
                    try:
                        # 30 second timeout per batch
                        sent_count = future.result(timeout=30)
                        total_sent += sent_count
                    except Exception as e:
                        failed_batch = future_to_batch[future]
                        failed_emails.extend(failed_batch)
                        logger.error(f'Batch failed: {str(e)}')

            logger.info(
                f'Bulk email completed. Sent: {total_sent}, Failed: {len(failed_emails)}')

            return JsonResponse({
                'success': True,
                'message': f'Bulk email completed successfully',
                'total_sent': total_sent,
                'total_failed': len(failed_emails),
                # Return first 10 failed emails
                'failed_emails': failed_emails[:10]
            })

        except Exception as e:
            logger.error(f'Error in bulk email sending: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

    # GET request - show form
    return render(request, 'emails/send_bulk.html', {
        'total_subscribers': len(EMAIL_LIST)
    })
