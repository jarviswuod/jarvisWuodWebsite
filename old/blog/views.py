# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Blog, Like, Comment, Share
from .forms import CommentForm


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

    return render(request, 'blog/blog_detail.html', context)


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

    return render(request, 'blog/blog_list.html', context)
