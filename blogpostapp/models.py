from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .util import *
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now
from django.utils import timezone
import pytz
from pytz import timezone
from datetime import datetime
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    mobile= models.PositiveBigIntegerField('mobile',null=True,blank=True)
    image=models.ImageField(default="profile_pics.jpg", upload_to="profile_pics/")
    bio = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    twitter = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    Title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    thumbnail=models.ImageField(default="category_pics.jpg", upload_to="category_pics/")
    
    def __str__(self):
        return self.Title

class Blog(models.Model):
    Title = models.CharField(max_length=150,blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    # Desc = models.CharField(max_length=150,blank=True)
    # Desc = RichTextField(blank=True,null=True)
    Desc = RichTextUploadingField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    
    auditby = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='audit_blogs', null=True, blank=True)
    publishedby = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='published_blogs', null=True, blank=True)

    blockimage=models.ImageField(default="block_pics.jpg", upload_to="block_pics/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="Category")
    favourite=models.ManyToManyField(User,related_name='favourite',default=None, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    publish_date = models.DateTimeField(auto_now= True)
    approved_date = models.DateTimeField(auto_now= True)
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_on']
    
    def preview(self):
        return ' '.join(self.Desc.split('.')[:1])

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse("blogpostapp:show_post")

    def was_published_recently(self):
        return self.created_at >= timezone.now() - timezone.timedelta(days=1)

    # def get_absolute_url(self):
    #     return reverse("article_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.Title)
        
        return super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='replies')   
    
    body = models.TextField()
    created = models.DateTimeField(default=now)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment by {}'.format(self.user.username)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_text = models.TextField()
    
    def __str__(self):
        return 'Reply on comment user {} and on blog {}'.format(self.comment.user,self.comment.blog)

class FavoriteBlog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.blog.Title}'