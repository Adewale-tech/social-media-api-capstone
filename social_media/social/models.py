# =================================================================
# social/models.py - Database Models with Explanations
# =================================================================

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# EXPLANATION: Custom User Model
# We extend AbstractUser instead of creating from scratch to get Django's
# built-in authentication features (login, password hashing, etc.)
class User(AbstractUser):
    # EXPLANATION: Additional fields beyond Django's default User
    # bio, profile_picture, etc. are for stretch goal "Profile Customization"
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cover_photo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Most recent users first
    
    def __str__(self):
        return self.username

# EXPLANATION: Post Model
# Represents individual posts in the social media platform
class Post(models.Model):
    content = models.TextField()  # Main post content (required)
    
    # EXPLANATION: Foreign Key relationship
    # Each post belongs to one user (author), but user can have many posts
    # CASCADE means if user is deleted, their posts are deleted too
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    timestamp = models.DateTimeField(auto_now_add=True)  # Set once when created
    updated_at = models.DateTimeField(auto_now=True)     # Updates every time saved
    media_url = models.URLField(blank=True, null=True)   # Optional media attachment
    
    class Meta:
        ordering = ['-timestamp']  # Most recent posts first (for feed)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."

# EXPLANATION: Follow Model  
# Represents follower-following relationships between users
class Follow(models.Model):
    # EXPLANATION: Two foreign keys to same model (User)
    # follower = person who follows, followed = person being followed
    # related_name prevents conflicts since both point to User
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # EXPLANATION: Prevents duplicate follows and ensures database efficiency
        unique_together = ('follower', 'followed')
    
    def clean(self):
        # EXPLANATION: Prevents users from following themselves
        if self.follower == self.followed:
            raise ValidationError("Users cannot follow themselves.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

# EXPLANATION: Like Model (Stretch Goal Feature)
# Allows users to like posts
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # EXPLANATION: One user can only like a post once
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

# EXPLANATION: Comment Model (Stretch Goal Feature)  
# Allows users to comment on posts
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Most recent comments first
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."