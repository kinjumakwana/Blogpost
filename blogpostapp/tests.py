from django.test import TestCase

# Create your tests here.
from django.shortcuts import render
from .models import BlogPost
from .forms import BlogPostForm

def change_blog(request, pk):
    blog_post = BlogPost.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user.is_author:
            form = BlogPostForm(instance=blog_post)
        elif request.user.is_editor:
            form = BlogPostForm(instance=blog_post, editor=True)
        elif request.user.is_publisher:
            form = BlogPostForm(instance=blog_post, publisher=True)
        else:
            form = None
    else:
        form = None
    return render(request, 'change_blog.html', {'form': form})

# form.py
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'status']

    def __init__(self, *args, **kwargs):
        editor = kwargs.pop('editor', False)
        publisher = kwargs.pop('publisher', False)
        super().__init__(*args, **kwargs)
        
        if editor:
            self.fields['status'].widget = forms.HiddenInput()
        if publisher:
            self.fields['status'].widget = forms.HiddenInput()

# {% if form %}
#     <form method="post" action="{% url 'change_blog' pk=blog_post.pk %}">
#         {% csrf_token %}
#         {{ form.as_p }}
#         <input type="submit" value="Save Changes">
#     </form>
# {% endif %}

# from django.urls import path
# from .views import change_blog

# urlpatterns = [
#     path('change_blog/<int:pk>', change_blog, name='change_blog'),
# ]