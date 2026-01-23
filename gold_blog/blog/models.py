from django.db import models 
from django.urls import reverse 
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager
class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED) 
            )
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date='publish' 
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default = Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
         
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse(
            "blog:post_detail", 
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
    )
    tags = TaggableManager()
#creating a model for comments.
class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'  # Reverse access: post.comments.all() instead of post.comment_set.all()
    )
    name = models.CharField(max_length=80)  # Commenter's name
    email = models.EmailField()  # Commenter's email
    body = models.TextField()  # Comment content
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when last updated
    active = models.BooleanField(default=True)  # Moderation flag

    class Meta:
        ordering = ['created']  # Oldest comments first
        indexes = [
            models.Index(fields=['created']),  # Optimize queries by creation time
        ]
    def __str__(self):
        return f'Commented by {self.name} on {self.post}'  # Human-readable label
    #makemigration
#next go to admin.py and register the model
