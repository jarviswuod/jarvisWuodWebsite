# admin.py
from django.contrib import admin
from .models import Blog, Like, Comment, Share


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published',
                    'created_at', 'total_likes', 'total_comments']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'author', 'content_preview',
                    'is_active', 'created_at', 'has_parent']
    list_filter = ['is_active', 'created_at', 'blog']
    search_fields = ['content', 'author__username', 'blog__title']
    ordering = ['-created_at']
    actions = ['mark_active', 'mark_inactive']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

    def has_parent(self, obj):
        return obj.parent is not None
    has_parent.boolean = True
    has_parent.short_description = 'Is Reply'

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = 'Mark selected comments as active'

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = 'Mark selected comments as inactive'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_at']
    list_filter = ['created_at', 'blog']
    search_fields = ['user__username', 'blog__title']
    ordering = ['-created_at']


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'platform', 'created_at']
    list_filter = ['platform', 'created_at', 'blog']
    search_fields = ['user__username', 'blog__title']
    ordering = ['-created_at']
