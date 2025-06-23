from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.html import strip_tags
import logging

from django.db.models import Q
from .models import NewsletterSubscriber, Blog, Like, Comment, Share
from .forms import NewsletterForm, CommentForm

logger = logging.getLogger(__name__)


def blogs(request):
    form = NewsletterForm()
    blogs = Blog.objects.filter(is_published=True)

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            subscriber = form.save()
            send_newsletter_confirmation_email(
                request, subscriber.email_address)
            return redirect('newsletter_success')
        else:
            messages.error(
                request, "You are already subscribed to our newsletter or invalid email.")

    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    blogs_page = paginator.get_page(page_number)

    context = {
        'form': form,
        'blogs': blogs_page,
        'search_query': search_query,
    }

    return render(request, 'blogs/blogs.html', context)


def blog_detail(request, slug):

    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    comments = blog.comments.filter(is_active=True, parent=None)
    comment_form = CommentForm()

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(
            user=request.user, blog=blog).exists()

    # Comment handling
    add_comment(request, blog, slug)

    # Pagination
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)

    # User modal handling
    modal_response = handle_user_modal_forms(request, slug)
    if modal_response:
        return modal_response

    context = {
        'blog': blog,
        'comments': comments_page,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'total_likes': blog.total_likes(),
        'total_comments': blog.total_comments(),
    }

    return render(request, 'blogs/blog_detail.html', context)


def newsletter_subscription(request):
    form = NewsletterForm()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            subscriber = form.save()
            send_newsletter_confirmation_email(
                request, subscriber.email_address)
            return redirect('newsletter_success')
        else:
            messages.error(
                request, "You are already subscribed to our newsletter or invalid email.")

    context = {'form': form}
    return render(request, 'blogs/newsletter_subscription.html', context)


def newsletter_success(request):
    return render(request, 'blogs/newsletter_success.html')


# ////////////////////////////////////////////////////////////////////////////////////////////
# HELPER FUNCTIONS
# ////////////////////////////////////////////////////////////////////////////////////////////

def send_newsletter_confirmation_email(request, email_address):
    """
    Send newsletter confirmation email and handle success/error messaging
    """
    subject = "Welcome to Jarvis Wuod's Newsletter"
    message = f"""
    Hi there,

    Thank you for subscribing to my newsletter.

    You'll receive thoughtful content straight to your inbox every week.
    No spam, just valuable insights and updates on my latest blog posts.

    What to expect:
    - Weekly curated content
    - Exclusive insights and tips
    - Early access to new blog posts
    - Behind-the-scenes updates

    If you ever want to unsubscribe, simply click the unsubscribe link at the bottom of any newsletter email.

    Best regards,
    Jarvis Wuod
    """

    try:
        send_mail(subject, message, 'jarviswuod@gmail.com', [email_address])
        messages.success(
            request, "You have successfully subscribed to the weekly newsletter!")
    except Exception as e:
        messages.warning(
            request, "Subscription successful, but there was an issue sending the confirmation email.")


def handle_user_modal_forms(request, slug=None):
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login
    from django.contrib import messages
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.conf import settings
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    if request.method != 'POST':
        return None

    form_type = request.POST.get('form_type')

    if form_type == 'login_form':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
        else:
            messages.error(request, "Invalid username or password!")

    elif form_type == 'signup_form':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )

            login(request, user)
            messages.success(
                request, "Account created and logged in successfully!")

        except Exception as e:
            messages.error(request, "Registration failed. Please try again.")

    elif form_type == 'password_reset_form':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{request.build_absolute_uri('/')[:-1]}/password-reset-confirm/{uid}/{token}/"

            html_message = render_to_string('users/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
                'domain': request.get_host(),
                'protocol': 'https' if request.is_secure() else 'http',
                'uid': uid,
                'token': token,
                'uidb64': uid,
            })
            plain_message = strip_tags(html_message)

            send_mail(
                subject='Your Password Reset Request on Jarvis Wuod',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(
                request, "Please check your email, Password reset email sent successfully!")

        except User.DoesNotExist:
            messages.error(request, "No user found with this email address!")
        except Exception as e:
            messages.error(
                request, f"Failed to send reset email. Please try again. {e}")

    return redirect(f"{reverse('blog_detail', kwargs={'slug': slug})}#engagementSection")

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ACTION VIEWS
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


@login_required
@require_POST
def add_comment(request, blog, slug):

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()

            send_comment_notifications(request, new_comment)
            return redirect(f"{reverse('blog_detail', kwargs={'slug': slug})}#commentsSection")


def send_comment_notifications(request, comment):
    current_site = get_current_site(request)
    blog_url = f"https://{current_site.domain}/blog/{comment.blog.slug}/"

    # 1. Notify blog author on comment
    if comment.blog.author.email and comment.blog.author != comment.author:
        send_blog_author_notification(comment, blog_url)

    # 2. Notify the parent comment author
    if comment.parent and comment.parent.author.email and comment.parent.author != comment.author:
        send_reply_notification(comment, blog_url)

    # 3. Notify other commenters in thread
    notify_thread_participants(comment, blog_url)


def send_blog_author_notification(comment, blog_url):
    try:
        subject = f'New comment on your blog: "{comment.blog.title}"'

        html_message = render_to_string('blogs/new_comment_notification.html', {
            'blog_author': comment.blog.author,
            'comment': comment,
            'blog': comment.blog,
            'blog_url': blog_url,
        })

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.blog.author.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(
            f"Blog author notification sent to {comment.blog.author.email}")

    except Exception as e:
        logger.error(f"Failed to send blog author notification: {str(e)}")


def send_reply_notification(comment, blog_url):
    try:
        subject = f'Reply to your comment on "{comment.blog.title}"'

        html_message = render_to_string('blogs/reply_notification.html', {
            'parent_author': comment.parent.author,
            'comment': comment,
            'parent_comment': comment.parent,
            'blog': comment.blog,
            'blog_url': blog_url,
        })

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.parent.author.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(
            f"Reply notification sent to {comment.parent.author.email}")

    except Exception as e:
        logger.error(f"Failed to send reply notification: {str(e)}")


def notify_thread_participants(comment, blog_url):
    try:
        thread_participants = Comment.objects.filter(
            blog=comment.blog
        ).exclude(
            author=comment.author
        ).exclude(
            author=comment.blog.author
        ).values_list('author__email', flat=True).distinct()

        # Remove empty emails
        participant_emails = [email for email in thread_participants if email]

        if participant_emails:
            subject = f'New comment on "{comment.blog.title}"'

            html_message = render_to_string('blogs/thread_notification.html', {
                'comment': comment,
                'blog': comment.blog,
                'blog_url': blog_url,
            })

            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=participant_emails,
                html_message=html_message,
                fail_silently=False,
            )

            logger.info(
                f"Thread notifications sent to {len(participant_emails)} participants")

    except Exception as e:
        logger.error(f"Failed to send thread notifications: {str(e)}")


@login_required
@require_POST
def toggle_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': blog.total_likes()
    })


@login_required
@require_POST
def share_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    platform = request.POST.get('platform')

    if platform in ['facebook', 'twitter', 'linkedin', 'whatsapp', 'email', 'copy_link']:
        Share.objects.create(
            user=request.user,
            blog=blog,
            platform=platform
        )
        return JsonResponse({'success': True, 'message': f'Blog shared on {platform}'})

    return JsonResponse({'success': False, 'error': 'Invalid platform'})
