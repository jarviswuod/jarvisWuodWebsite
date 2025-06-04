
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.db.models import Q
from .models import NewsletterSubscriber, Blog, Like, Comment, Share
from .forms import NewsletterForm, CommentForm


def blogs(request):
    form = NewsletterForm()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            subscriber = form.save()
            send_newsletter_confirmation_email(
                request, subscriber.email_address)
            return redirect('newsletter_success')  # Redirect to success page
        else:
            messages.error(
                request, "You are already subscribed to our newsletter or invalid email.")

    context = {'form': form}
    return render(request, 'blogs/blogs.html', context)


def newsletter_subscription(request):
    """
    Dedicated newsletter subscription page
    """
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
    """
    Success page for new newsletter subscribers
    """
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

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ADDED SCRIPTS FROM CLAUDE AI BLOG
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////


def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    blogs_page = paginator.get_page(page_number)

    context = {
        'blogs': blogs_page,
        'search_query': search_query,
    }

    return render(request, 'blogs/blog_list.html', context)
    # return render(request, 'blogs/_blog_list.html', context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    comments = blog.comments.filter(is_active=True, parent=None)

    # Check if user has liked the blog
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(
            user=request.user, blog=blog).exists()

    # Handle comment form
    comment_form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user

            # Handle reply to comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()
            messages.success(
                request, 'Your comment has been added successfully!')
            return redirect('blog_detail', slug=slug)

    # Pagination for comments
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)

    context = {
        'blog': blog,
        'comments': comments_page,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'total_likes': blog.total_likes(),
        'total_comments': blog.total_comments(),
    }

    # return render(request, 'blogs/_blog_detail.html', context)
    return render(request, 'blogs/blog_detail.html', context)


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
def add_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')

    if not content:
        return JsonResponse({'success': False, 'error': 'Comment content is required'})

    comment = Comment.objects.create(
        blog=blog,
        author=request.user,
        content=content
    )

    if parent_id:
        try:
            parent_comment = Comment.objects.get(id=parent_id)
            comment.parent = parent_comment
            comment.save()
        except Comment.DoesNotExist:
            pass

    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'parent_id': comment.parent.id if comment.parent else None
        }
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
