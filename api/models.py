from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model with Custom Roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('free', 'Free User'),
        ('premium', 'Premium Subscriber'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='free')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Subscription Model
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    SUBSCRIPTION_TYPE = [
        ('monthly', 'Monthly'),
        ('lifetime', 'Lifetime'),
        ('one_time', 'One-time Payment'),
    ]
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPE)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('expired', 'Expired')], default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('stripe', 'Stripe'), ('paypal', 'PayPal')])
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    access_type = models.CharField(max_length=10, choices=[('free', 'Free'), ('premium', 'Premium')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    content = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# User Course Progress Model
class UserCourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    progress_percentage = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

# Forum Models
class ForumThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ForumReply(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Comment Model (For Blog, Courses, Lessons, AI Projects)
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content_type = models.CharField(max_length=50, choices=[('blog', 'Blog'), ('course', 'Course'), ('lesson', 'Lesson'), ('project', 'Project')])
    object_id = models.PositiveIntegerField()  # Generic relation to different models
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# AI Projects Model
class AIProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_projects')
    github_repo_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Blog Model
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
