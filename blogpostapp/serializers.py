from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.utils import timezone

class Commentserializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField()
  created = serializers.DateTimeField(format='%b. %d %Y, %H:%M:%S %p')
  user_picture = serializers.SerializerMethodField(
        'get_picture')
  user_id = serializers.SerializerMethodField(
        'get_userid')
  c_id = serializers.SerializerMethodField(
        'get_cid')

  class Meta:
    model = Comment
    fields = ['created','user','blog','body','user_picture','user_id','id','c_id']

  def get_picture(self, comment):
      return comment.user.image.url
  
  def get_userid(self, comment):
      return comment.user.id

  def get_cid(self, comment):
      return comment.id

class BlogSerializer(serializers.ModelSerializer):
      created_on = serializers.DateTimeField(format='%b. %d %Y, %H:%M:%S %p')
      author = serializers.StringRelatedField()
      category = serializers.StringRelatedField()
      auditby = serializers.StringRelatedField()
      publishedby=serializers.StringRelatedField()
      blog_image = serializers.SerializerMethodField(
        'get_bpicture')
        
      class Meta:
            model = Blog
            fields = ['preview','id','created_on','Title','slug','Desc','author','auditby','publishedby','blockimage','category','favourite','updated_on','publish_date','approved_date','is_approved','is_published','blog_image']

      def get_bpicture(self, blog):
            return blog.blockimage.url