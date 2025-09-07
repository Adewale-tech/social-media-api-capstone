# =================================================================
# FILE: social/admin.py
# PURPOSE: Configure Django Admin interface for managing your models
# LOCATION: social_media_api/social/admin.py
# =================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Follow, Like, Comment

# EXPLANATION: Custom User Admin Configuration
# This extends Django's built-in UserAdmin to include your custom fields
class CustomUserAdmin(UserAdmin):
    # EXPLANATION: Display these fields in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'is_staff', 'date_joined', 'posts_count', 'followers_count')
    
    # EXPLANATION: Add filters in the right sidebar for easy searching
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'location')
    
    # EXPLANATION: Enable search functionality
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # EXPLANATION: Order users by most recent first
    ordering = ('-date_joined',)
    
    # EXPLANATION: Add your custom fields to the user edit form
    # This extends the default UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'profile_picture', 'location', 'website', 'cover_photo'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # EXPLANATION: Add custom fields to the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('email', 'bio', 'location'),
        }),
    )
    
    # EXPLANATION: Custom methods to show additional info in list view
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Posts'  # Column header name
    
    def followers_count(self, obj):
        return obj.followers.count()
    followers_count.short_description = 'Followers'

# EXPLANATION: Post Admin Configuration
class PostAdmin(admin.ModelAdmin):
    # EXPLANATION: Fields shown in the post list view
    list_display = ('content_preview', 'user', 'timestamp', 'likes_count', 'comments_count')
    
    # EXPLANATION: Filters for the right sidebar
    list_filter = ('timestamp', 'updated_at')
    
    # EXPLANATION: Enable search by content and author
    search_fields = ('content', 'user__username', 'user__email')
    
    # EXPLANATION: Default ordering (newest first)
    ordering = ('-timestamp',)
    
    # EXPLANATION: Fields that are read-only (can't be edited)
    readonly_fields = ('timestamp', 'updated_at')
    
    # EXPLANATION: How many posts to show per page
    list_per_page = 25
    
    # EXPLANATION: Custom method to show post preview
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    # EXPLANATION: Custom methods to show counts
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'

# EXPLANATION: Follow Admin Configuration
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'followed__username')
    ordering = ('-created_at',)
    
    # EXPLANATION: Prevent editing of follow relationships (only view/delete)
    readonly_fields = ('created_at',)
    
    # EXPLANATION: Custom validation in admin
    def save_model(self, request, obj, form, change):
        # EXPLANATION: Prevent self-following even in admin
        if obj.follower == obj.followed:
            from django.contrib import messages
            messages.error(request, "Users cannot follow themselves.")
            return
        super().save_model(request, obj, form, change)

# EXPLANATION: Like Admin Configuration
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def post_preview(self, obj):
        return f"{obj.post.content[:30]}..." if len(obj.post.content) > 30 else obj.post.content
    post_preview.short_description = 'Post'

# EXPLANATION: Comment Admin Configuration
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_preview', 'content_preview', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'content', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'Comment'
    
    def post_preview(self, obj):
        return f"{obj.post.content[:20]}..." if len(obj.post.content) > 20 else obj.post.content
    post_preview.short_description = 'Post'

# EXPLANATION: Register all models with their custom admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)

# EXPLANATION: Customize admin site headers
admin.site.site_header = "Social Media API Administration"
admin.site.site_title = "Social Media Admin"
admin.site.index_title = "Welcome to Social Media API Admin Panel"


# Register your models here.
