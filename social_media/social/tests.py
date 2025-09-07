# =================================================================
# FILE: social/tests.py
# PURPOSE: Unit tests for Social Media API functionality
# LOCATION: social_media_api/social/tests.py
# =================================================================

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Follow, Like, Comment

User = get_user_model()

# EXPLANATION: Base Test Class for Common Setup
class BaseTestCase(APITestCase):
    """
    Base test case that sets up common test data and utilities
    """
    
    def setUp(self):
        # EXPLANATION: Create test users for all tests
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # EXPLANATION: Create authentication tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # EXPLANATION: Set up API client for making requests
        self.client = APIClient()
    
    def authenticate_user1(self):
        """Helper method to authenticate as user1"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
    
    def authenticate_user2(self):
        """Helper method to authenticate as user2"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')

# EXPLANATION: Test User Model and Authentication
class UserModelTestCase(TestCase):
    """
    Test cases for User model functionality
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            bio='Test user bio',
            location='Test City'
        )
    
    def test_user_creation(self):
        """EXPLANATION: Test that user is created with correct attributes"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.bio, 'Test user bio')
        self.assertEqual(self.user.location, 'Test City')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str_method(self):
        """EXPLANATION: Test __str__ method returns username"""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_counts_properties(self):
        """EXPLANATION: Test that user count properties work correctly"""
        # Initially should be 0
        self.assertEqual(self.user.posts.count(), 0)
        self.assertEqual(self.user.followers.count(), 0)
        self.assertEqual(self.user.following.count(), 0)

# EXPLANATION: Test User Registration and Authentication APIs
class UserAuthenticationTestCase(BaseTestCase):
    """
    Test cases for user registration and login functionality
    """
    
    def test_user_registration(self):
        """EXPLANATION: Test user can register successfully"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'bio': 'New user bio'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
    
    def test_user_registration_password_mismatch(self):
        """EXPLANATION: Test registration fails with password mismatch"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """EXPLANATION: Test user can login successfully"""
        url = reverse('login')
        data = {
            'username': 'testuser1',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
    
    def test_user_login_invalid_credentials(self):
        """EXPLANATION: Test login fails with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'testuser1',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# EXPLANATION: Test Post Model and CRUD Operations
class PostModelTestCase(BaseTestCase):
    """
    Test cases for Post model and CRUD operations
    """
    
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            content='Test post content',
            user=self.user1
        )
    
    def test_post_creation(self):
        """EXPLANATION: Test post is created correctly"""
        self.assertEqual(self.post.content, 'Test post content')
        self.assertEqual(self.post.user, self.user1)
        self.assertIsNotNone(self.post.timestamp)
    
    def test_post_str_method(self):
        """EXPLANATION: Test __str__ method shows username and content preview"""
        expected = f"{self.user1.username}: Test post content..."
        self.assertEqual(str(self.post), expected)

# EXPLANATION: Test Post API Endpoints
class PostAPITestCase(BaseTestCase):
    """
    Test cases for Post API endpoints
    """
    
    def test_create_post_authenticated(self):
        """EXPLANATION: Test authenticated user can create post"""
        self.authenticate_user1()
        url = reverse('post-list-create')
        data = {
            'content': 'New test post',
            'media_url': 'https://example.com/image.jpg'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        
        post = Post.objects.first()
        self.assertEqual(post.content, 'New test post')
        self.assertEqual(post.user, self.user1)
    
    def test_create_post_unauthenticated(self):
        """EXPLANATION: Test unauthenticated user cannot create post"""
        url = reverse('post-list-create')
        data = {'content': 'New test post'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_posts(self):
        """EXPLANATION: Test listing all posts"""
        # Create test posts
        Post.objects.create(content='Post 1', user=self.user1)
        Post.objects.create(content='Post 2', user=self.user2)
        
        self.authenticate_user1()
        url = reverse('post-list-create')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_update_own_post(self):
        """EXPLANATION: Test user can update their own post"""
        post = Post.objects.create(content='Original content', user=self.user1)
        
        self.authenticate_user1()
        url = reverse('post-detail', kwargs={'pk': post.id})
        data = {'content': 'Updated content'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        post.refresh_from_db()
        self.assertEqual(post.content, 'Updated content')
    
    def test_delete_own_post(self):
        """EXPLANATION: Test user can delete their own post"""
        post = Post.objects.create(content='To be deleted', user=self.user1)
        
        self.authenticate_user1()
        url = reverse('post-detail', kwargs={'pk': post.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

# EXPLANATION: Test Follow System
class FollowSystemTestCase(BaseTestCase):
    """
    Test cases for follow/unfollow functionality
    """
    
    def test_follow_user(self):
        """EXPLANATION: Test user can follow another user"""
        self.authenticate_user1()
        url = reverse('follow-user', kwargs={'user_id': self.user2.id})
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Follow.objects.filter(follower=self.user1, followed=self.user2).exists()
        )
    
    def test_cannot_follow_self(self):
        """EXPLANATION: Test user cannot follow themselves"""
        self.authenticate_user1()
        url = reverse('follow-user', kwargs={'user_id': self.user1.id})
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot follow yourself', response.data['error'])
    
    def test_unfollow_user(self):
        """EXPLANATION: Test user can unfollow another user"""
        # First, create a follow relationship
        Follow.objects.create(follower=self.user1, followed=self.user2)
        
        self.authenticate_user1()
        url = reverse('unfollow-user', kwargs={'user_id': self.user2.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Follow.objects.filter(follower=self.user1, followed=self.user2).exists()
        )
    
    def test_unfollow_not_following(self):
        """EXPLANATION: Test unfollowing user not being followed"""
        self.authenticate_user1()
        url = reverse('unfollow-user', kwargs={'user_id': self.user2.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# EXPLANATION: Test User Feed Functionality
class UserFeedTestCase(BaseTestCase):
    """
    Test cases for user feed functionality
    """
    
    def test_user_feed_shows_followed_users_posts(self):
        """EXPLANATION: Test feed shows posts from followed users"""
        # User1 follows User2
        Follow.objects.create(follower=self.user1, followed=self.user2)
        
        # User2 creates a post
        post = Post.objects.create(content='Post from followed user', user=self.user2)
        
        self.authenticate_user1()
        url = reverse('user-feed')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], post.id)
    
    def test_user_feed_shows_own_posts(self):
        """EXPLANATION: Test feed includes user's own posts"""
        # User1 creates a post
        post = Post.objects.create(content='Own post', user=self.user1)
        
        self.authenticate_user1()
        url = reverse('user-feed')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], post.id)
    
    def test_user_feed_excludes_unfollowed_users_posts(self):
        """EXPLANATION: Test feed excludes posts from unfollowed users"""
        # User2 creates a post but User1 doesn't follow User2
        Post.objects.create(content='Post from unfollowed user', user=self.user2)
        
        self.authenticate_user1()
        url = reverse('user-feed')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

# EXPLANATION: Test Like System (Stretch Goal)
class LikeSystemTestCase(BaseTestCase):
    """
    Test cases for like/unlike functionality
    """
    
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(content='Test post', user=self.user1)
    
    def test_like_post(self):
        """EXPLANATION: Test user can like a post"""
        self.authenticate_user2()
        url = reverse('like-post', kwargs={'post_id': self.post.id})
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Like.objects.filter(user=self.user2, post=self.post).exists()
        )
    
    def test_unlike_post(self):
        """EXPLANATION: Test user can unlike a previously liked post"""
        # First like the post
        Like.objects.create(user=self.user2, post=self.post)
        
        self.authenticate_user2()
        url = reverse('like-post', kwargs={'post_id': self.post.id})
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Like.objects.filter(user=self.user2, post=self.post).exists()
        )

# EXPLANATION: Test Comment System (Stretch Goal)
class CommentSystemTestCase(BaseTestCase):
    """
    Test cases for comment functionality
    """
    
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(content='Test post', user=self.user1)
    
    def test_create_comment(self):
        """EXPLANATION: Test user can comment on a post"""
        self.authenticate_user2()
        url = reverse('post-comments', kwargs={'post_id': self.post.id})
        data = {'content': 'Test comment'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.user, self.user2)
        self.assertEqual(comment.post, self.post)
    
    def test_list_post_comments(self):
        """EXPLANATION: Test listing comments for a post"""
        # Create test comments
        Comment.objects.create(content='Comment 1', user=self.user1, post=self.post)
        Comment.objects.create(content='Comment 2', user=self.user2, post=self.post)
        
        self.authenticate_user1()
        url = reverse('post-comments', kwargs={'post_id': self.post.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

# EXPLANATION: Test Follow Model Constraints
class FollowModelTestCase(TestCase):
    """
    Test cases for Follow model constraints and validation
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email='user1@test.com', password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@test.com', password='pass123'
        )
    
    def test_follow_creation(self):
        """EXPLANATION: Test follow relationship is created correctly"""
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.followed, self.user2)
    
    def test_follow_str_method(self):
        """EXPLANATION: Test __str__ method shows follow relationship"""
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        expected = f"{self.user1.username} follows {self.user2.username}"
        self.assertEqual(str(follow), expected)
    
    def test_cannot_follow_self_validation(self):
        """EXPLANATION: Test model validation prevents self-following"""
        from django.core.exceptions import ValidationError
        
        follow = Follow(follower=self.user1, followed=self.user1)
        with self.assertRaises(ValidationError):
            follow.save()

# EXPLANATION: Test API Permissions
class APIPermissionTestCase(BaseTestCase):
    """
    Test cases for API permission and authentication
    """
    
    def test_unauthenticated_access_denied(self):
        """EXPLANATION: Test all protected endpoints require authentication"""
        endpoints = [
            reverse('post-list-create'),
            reverse('user-feed'),
        ]
        
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Create your tests here.
