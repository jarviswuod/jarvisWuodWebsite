from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import csv
import base64
from io import BytesIO
from PIL import Image

from .models import Newsletter, Subscriber, EmailSent, EmailOpen, LinkClick, UnsubscribeFeedback
from .forms import NewsletterForm, SubscribeForm, UnsubscribeFeedbackForm
from .utils import send_newsletter_email, get_client_ip


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber, created = Subscriber.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'is_active': True
                }
            )

            if created:
                messages.success(
                    request, 'Successfully subscribed to our newsletter!')
            else:
                if not subscriber.is_active:
                    subscriber.is_active = True
                    subscriber.save()
                    messages.success(
                        request, 'Welcome back! You have been resubscribed.')
                else:
                    messages.info(
                        request, 'You are already subscribed to our newsletter.')
            return redirect('newsletters:subscribe')
    else:
        form = SubscribeForm()

    return render(request, 'newsletters/subscribe.html', {'form': form})


def unsubscribe(request, token):
    subscriber = get_object_or_404(Subscriber, unsubscribe_token=token)

    if request.method == 'POST':
        return redirect('newsletters:unsubscribe_feedback', token=token)

    return render(request, 'newsletters/unsubscribe.html', {'subscriber': subscriber})


def unsubscribe_feedback(request, token):
    subscriber = get_object_or_404(Subscriber, unsubscribe_token=token)

    if request.method == 'POST':
        form = UnsubscribeFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.subscriber = subscriber
            feedback.save()

            # Actually unsubscribe the user
            subscriber.is_active = False
            subscriber.save()

            messages.success(
                request, 'Thank you for your feedback. You have been unsubscribed.')
            return render(request, 'newsletters/unsubscribe_success.html')
    else:
        form = UnsubscribeFeedbackForm()

    return render(request, 'newsletters/unsubscribe_feedback.html', {
        'form': form,
        'subscriber': subscriber
    })

# Tracking Views


@csrf_exempt
def track_open(request, tracking_id):
    try:
        email_sent = EmailSent.objects.get(tracking_id=tracking_id)

        # Create tracking record
        EmailOpen.objects.create(
            email_sent=email_sent,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        # Update email_sent record
        if not email_sent.is_opened:
            email_sent.is_opened = True
            email_sent.opened_at = timezone.now()
        email_sent.open_count += 1
        email_sent.save()

    except EmailSent.DoesNotExist:
        pass

    # Return 1x1 transparent pixel
    img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')


@csrf_exempt
def track_click(request, tracking_id):
    url = request.GET.get('url')
    if not url:
        raise Http404

    try:
        email_sent = EmailSent.objects.get(tracking_id=tracking_id)

        LinkClick.objects.create(
            email_sent=email_sent,
            url=url,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except EmailSent.DoesNotExist:
        pass

    return redirect(url)

# Admin Views


@login_required
def newsletter_list(request):
    newsletters = Newsletter.objects.all()
    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    newsletters = paginator.get_page(page)

    return render(request, 'newsletters/list.html', {'newsletters': newsletters})


@login_required
def newsletter_create(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.created_by = request.user
            newsletter.save()
            messages.success(request, 'Newsletter created successfully!')
            return redirect('newsletters:detail', pk=newsletter.pk)
    else:
        form = NewsletterForm()

    return render(request, 'newsletters/create.html', {'form': form})


@login_required
def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    stats = None

    if newsletter.is_sent:
        stats = {
            'total_sent': newsletter.emails_sent.count(),
            'total_opens': EmailOpen.objects.filter(email_sent__newsletter=newsletter).count(),
            'unique_opens': newsletter.emails_sent.filter(is_opened=True).count(),
            'total_clicks': LinkClick.objects.filter(email_sent__newsletter=newsletter).count(),
        }
        if stats['total_sent'] > 0:
            stats['open_rate'] = (stats['unique_opens'] /
                                  stats['total_sent']) * 100
            stats['click_rate'] = (
                stats['total_clicks'] / stats['total_sent']) * 100

    return render(request, 'newsletters/detail.html', {
        'newsletter': newsletter,
        'stats': stats
    })


@login_required
def newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if newsletter.is_sent:
        messages.error(
            request, 'Cannot edit a newsletter that has already been sent.')
        return redirect('newsletters:detail', pk=pk)

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated successfully!')
            return redirect('newsletters:detail', pk=pk)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'newsletters/edit.html', {'form': form, 'newsletter': newsletter})


@login_required
def newsletter_send(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if newsletter.is_sent:
        messages.error(request, 'This newsletter has already been sent.')
        return redirect('newsletters:detail', pk=pk)

    if request.method == 'POST':
        active_subscribers = Subscriber.objects.filter(is_active=True)

        for subscriber in active_subscribers:
            success = send_newsletter_email(newsletter, subscriber)
            if success:
                EmailSent.objects.create(
                    newsletter=newsletter,
                    subscriber=subscriber
                )

        newsletter.is_sent = True
        newsletter.sent_at = timezone.now()
        newsletter.save()

        messages.success(
            request, f'Newsletter sent to {active_subscribers.count()} subscribers!')
        return redirect('newsletters:detail', pk=pk)

    subscriber_count = Subscriber.objects.filter(is_active=True).count()
    return render(request, 'newsletters/send_confirm.html', {
        'newsletter': newsletter,
        'subscriber_count': subscriber_count
    })


@login_required
def newsletter_analytics(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if not newsletter.is_sent:
        messages.error(
            request, 'Analytics are only available for sent newsletters.')
        return redirect('newsletters:detail', pk=pk)

    emails_sent = newsletter.emails_sent.all()
    opens = EmailOpen.objects.filter(
        email_sent__newsletter=newsletter).order_by('-opened_at')
    clicks = LinkClick.objects.filter(
        email_sent__newsletter=newsletter).order_by('-clicked_at')

    return render(request, 'newsletters/analytics.html', {
        'newsletter': newsletter,
        'emails_sent': emails_sent,
        'opens': opens[:50],  # Show last 50 opens
        'clicks': clicks[:50],  # Show last 50 clicks
    })


@login_required
def subscriber_list(request):
    subscribers = Subscriber.objects.all().order_by('-date_subscribed')

    # Search functionality
    search = request.GET.get('search')
    if search:
        subscribers = subscribers.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    # Filter by status
    status = request.GET.get('status')
    if status == 'active':
        subscribers = subscribers.filter(is_active=True)
    elif status == 'inactive':
        subscribers = subscribers.filter(is_active=False)

    paginator = Paginator(subscribers, 25)
    page = request.GET.get('page')
    subscribers = paginator.get_page(page)

    return render(request, 'newsletters/subscriber_list.html', {'subscribers': subscribers})


@login_required
def export_subscribers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'First Name', 'Last Name',
                    'Status', 'Date Subscribed'])

    for subscriber in Subscriber.objects.all():
        writer.writerow([
            subscriber.email,
            subscriber.first_name,
            subscriber.last_name,
            'Active' if subscriber.is_active else 'Inactive',
            subscriber.date_subscribed.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@login_required
def feedback_list(request):
    feedback = UnsubscribeFeedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedback, 25)
    page = request.GET.get('page')
    feedback = paginator.get_page(page)

    return render(request, 'newsletters/feedback_list.html', {'feedback': feedback})
