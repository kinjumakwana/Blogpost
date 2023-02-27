from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth import get_user_model
from.models import *

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'last_name', 'email','mobile','image','bio','password1','password2','facebook','twitter','instagram','linkedin']
        labels = {'email': 'Email Address',}

class CustomAuthForm(AuthenticationForm):
        # email = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
        # password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    def init(self, *args, **kwargs):
        super(CustomAuthForm, self).init(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class BlogForm(forms.ModelForm):
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
    class Meta:
        model = Blog
        fields = ['Title','Desc','blockimage','category']
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(BlogForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BlogForm, self).save(commit=False)
        instance.author = self.author
        if commit:
            instance.save()
        return instance

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Blog
        fields = ['Title','Desc','blockimage','category']

class EditorForm(forms.ModelForm):
    is_approved = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Blog
        fields = ['Title','Desc','blockimage','category','is_approved']
    
    def save(self, commit=True, *args, **kwargs):
        self.instance.auditby = self.initial['auditby']
        return super().save(commit=commit, *args, **kwargs)

class PublisherForm(forms.ModelForm):
    is_approved = forms.BooleanField()
    is_published = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Blog
        fields = ['Title','Desc','blockimage','category','is_approved','is_published']
    
    def save(self, commit=True, *args, **kwargs):
        self.instance.publishedby = self.initial['publishedby']
        return super().save(commit=commit, *args, **kwargs)

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['Title','subtitle','thumbnail']

class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'last_name', 'email','mobile','image','bio','facebook','twitter','instagram','linkedin']
        labels = {'email': 'Email Address',}

class ImageupdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['image']

class CommentForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ('body',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']