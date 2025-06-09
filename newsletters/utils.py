from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
import re
from urllib.parse import quote


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_tracking_to_html(html_content, tracking_id, request=None):
    """Add tracking pixel and link tracking to HTML content"""
    if not html_content:
        return html_content

    # Add tracking pixel at the end of the HTML
    base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
    if request:
        base_url = f"{request.scheme}://{request.get_host()}"

    tracking_pixel = f'<img src="{base_url}{reverse("newsletter:track_open", args=[tracking_id])}" width="1" height="1" style="display:none;" />'

    # Add tracking pixel before closing body tag or at the end
    if '</body>' in html_content:
        html_content = html_content.replace(
            '</body>', f'{tracking_pixel}</body>')
    else:
        html_content += tracking_pixel

    # Replace links with tracking links
    def replace_link(match):
        original_url = match.group(1)
        if original_url.startswith('mailto:') or original_url.startswith('#'):
            return match.group(0)  # Don't track mailto or anchor links

        tracking_url = f"{base_url}{reverse('newsletter:track_click', args=[tracking_id])}?url={quote(original_url)}"
        return f'href="{tracking_url}"'

    html_content = re.sub(r'href="([^"]*)"', replace_link, html_content)

    return html_content


def send_newsletter_email(newsletter, subscriber):
    """Send newsletter email to a subscriber"""
    try:
        # Get the EmailSent record or create one
        from .models import EmailSent
        email_sent, created = EmailSent.objects.get_or_create(
            newsletter=newsletter,
            subscriber=subscriber
        )

        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        unsubscribe_url = f"{base_url}{reverse('newsletter:unsubscribe', args=[subscriber.unsubscribe_token])}"

        context = {
            'newsletter': newsletter,
            'subscriber': subscriber,
            'unsubscribe_url': unsubscribe_url,
        }

        # Prepare email content
        subject = newsletter.subject
        from_email = getattr(
            settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        to_email = [subscriber.email]

        # Text content
        text_content = newsletter.content
        if not text_content:
            text_content = "Please enable HTML to view this newsletter."

        # Add unsubscribe link to text content
        text_content += f"\n\nTo unsubscribe, visit: {unsubscribe_url}"

        # HTML content with tracking
        html_content = newsletter.html_content
        if html_content:
            html_content = add_tracking_to_html(
                html_content, email_sent.tracking_id)
            # Add unsubscribe link to HTML
            unsubscribe_html = f'<p style="font-size: 12px; color: #666; margin-top: 20px;"><a href="{unsubscribe_url}">Unsubscribe</a></p>'
            if '</body>' in html_content:
                html_content = html_content.replace(
                    '</body>', f'{unsubscribe_html}</body>')
            else:
                html_content += unsubscribe_html

        # Create email
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, to_email)

        if html_content:
            msg.attach_alternative(html_content, "text/html")

        # Send email
        msg.send()
        return True

    except Exception as e:
        print(f"Error sending email to {subscriber.email}: {str(e)}")
        return False
