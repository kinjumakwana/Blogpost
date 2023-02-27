from django.http import HttpResponse,HttpResponseForbidden,Http404, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.views import generic
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .serializers import *
from .mypaginations import *
from rest_framework import generics
from cursor_pagination import CursorPaginator
from django.http import HttpRequest
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView 
from django.http import JsonResponse
import pytz
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
# from django.template.defaultfilters import timezone
from django.utils.timezone import get_current_timezone
import datetime
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('blogpostapp:login')
    template_name = 'sign_up.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

@login_required
def viewuser(request):
    user = request.user
    print(user)
    userdata1 = User.objects.get(username=user)
    print(userdata1)
    # context={'u':userdata1} 
    context={'u':request.user} 
    return render(request,"viewuser.html", context)

@login_required
def create_group_permission(request):
    author_group, created = Group.objects.get_or_create(name="Author")
    editor_group, created = Group.objects.get_or_create(name="Editor")
    publisher_group, created = Group.objects.get_or_create(name="Publisher")

    content_type = ContentType.objects.get_for_model(Blog)
    post_permission = Permission.objects.filter(content_type=content_type)
    print([perm.codename for perm in post_permission])
    # => ['add_blog','change_blog', 'delete_blog', 'view_blog']

    # Publisher: view,add,change,delete
    # Editor: view,change
    # Author: view,add,change

    for perm in post_permission:
        # Publisher: delete_blog
        if perm.codename == "delete_blog":
            publisher_group.permissions.add(perm)

        # Publisher: change_blog
        # Editor: change_blog
        # Author: change_blog
        elif perm.codename == "change_blog":
            editor_group.permissions.add(perm)
            publisher_group.permissions.add(perm)
            author_group.permissions.add(perm)
        
        # Publisher: add_post
        # Author: add_post
        elif perm.codename == "add_blog":
            author_group.permissions.add(perm)
            publisher_group.permissions.add(perm)

        else:
            editor_group.permissions.add(perm)
            publisher_group.permissions.add(perm)
            author_group.permissions.add(perm)

    return HttpResponse(" Group Created")

@login_required
def author_group(request):
#     # Assign editor role to specific user
  
    if request.method=="POST":
        username = request.POST['name']
        author_group, created = Group.objects.get_or_create(name="Author")
        # user = User.objects.get(username=request.user)
        user = User.objects.get(username=username)
        user.groups.add(author_group)
        return HttpResponse("Successfully Added into Group")
    else:
        return render(request,"author_group.html")

@login_required
def publisher_group(request):
#     # Assign editor role to specific user
  
    if request.method=="POST":
        username = request.POST['name']
        publisher_group, created = Group.objects.get_or_create(name="Publisher")
        # user = User.objects.get(username=request.user)
        user = User.objects.get(username=username)
        user.groups.add(publisher_group)
        return HttpResponse("Successfully Added into Group")
    else:
        return render(request,"publisher_group.html")


from django.utils import timezone
@login_required
def create_blog(request):
    form = BlogForm(request.POST,request.FILES or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        # return redirect('blog_detail', pk=blog.pk)
        return HttpResponse("successfully add blog")
    return render(request, 'blog_form.html', {'form': form})

@login_required
def create_category(request):
    form = CategoryForm(request.POST,request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.save()
        # return redirect('blog_detail', pk=blog.pk)
        return HttpResponse("successfully add Category")
    return render(request, 'cat_form.html', {'form': form})

@permission_required('blogpostapp.delete_blog')
def delete_blog(request, blog_id):
    # Check if the user is a publisher
    publisher_group, created = Group.objects.get_or_create(name="Publisher")
    is_in_publi_group = check_user_in_group(request.user,publisher_group)
    print(is_in_publi_group)
    
    if is_in_publi_group:
    # if request.user.is_publisher:
        # Get the blog object by its id
        blog = get_object_or_404(Blog, id=blog_id)
        # Delete the blog object
        blog.delete()
        # Redirect to the blog list page
        return redirect('blogpostapp:show_post')
    else:
        # Return a 403 Forbidden status if the user is not a publisher
        return HttpResponseForbidden()

def show_post(request):
    requested_post = None
    posts = Blog.objects.all()
    context={'post':posts} 
    # print(context)
    return render(request, "post.html",{'post':posts})

def blog(request):
    posts = Blog.objects.all()
    categories  = Category.objects.all()
    context={'post':posts, 
            'categories': categories} 
    print(context)
    return render(request, "blog.html",context)

def check_user_in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

@login_required
@permission_required('blogpostapp.change_blog')
def authorchange_blog(request,id):
    post = Blog.objects.get(pk=id)
    
    if request.user != post.author:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return render(request, 'post.html', {'form': form})
        # else:
    form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
@permission_required('blogpostapp.change_blog')
def editorchange_blog(request,id):
    post = Blog.objects.get(pk=id)
    
    if request.method == 'POST':
        form = EditorForm(request.POST, instance=post,initial={'auditby': request.user})
        if form.is_valid():
            form.save()
            return render(request, 'post.html', {'form': form})
        # else:
    form = EditorForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
@permission_required('blogpostapp.change_blog')
def publisherchange_blog(request,id):
    post = Blog.objects.get(pk=id)
    
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=post,initial={'publishedby': request.user})
        if form.is_valid():
            form.save()
    form = PublisherForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})
    
def blogdetial(request):
    # user = get_user_model().objects.get(username=request.user)user
    author_group, created = Group.objects.get_or_create(name="Author")
    user = User.objects.get(username=request.user)

    is_in_auth_group = check_user_in_group(user,author_group)
    print(is_in_auth_group)
    
    publisher_group, created = Group.objects.get_or_create(name="Publisher")
    is_in_publi_group = check_user_in_group(request.user,publisher_group)
    
    if is_in_auth_group or publisher_group:
        auth_post = Blog.objects.filter(author=user)
        # return redirect("authorchange_blog",pk=user)
        return render(request,"post.html",{'post':auth_post, 'is_auth':is_in_auth_group})
    
    else:
        return HttpResponse ("User is not in Author Group")

@login_required
@permission_required('blogpostapp.change_blog')
def masterchange_blog(request):
    author_group, created = Group.objects.get_or_create(name="Author")
    is_in_auth_group = check_user_in_group(request.user,author_group)
    
    editor_group, created = Group.objects.get_or_create(name="Editor")
    is_in_edi_group = check_user_in_group(request.user,editor_group)
    
    publisher_group, created = Group.objects.get_or_create(name="Publisher")
    is_in_publi_group = check_user_in_group(request.user,publisher_group)
    
    if is_in_auth_group:

        auth_post = Blog.objects.filter(author=request.user)
        auth_ids = auth_post.values_list('id', flat=True)
        print(auth_ids)
        first_object = auth_ids[0]
        print(first_object)
        return redirect("blogpostapp:authorchange_blog",id=first_object)
    
    elif is_in_edi_group:
        # auth_post = Blog.objects.filter(author=request.user)
        # blogid = request.POST.get('id')
        post = Blog.objects.get(pk=blogid)
        return redirect("editorchange_blog",pk=post.id)
    
    elif is_in_publi_group:
        auth_post = Blog.objects.filter(author=request.user)
        blogid = request.POST.get('id')
        post = Blog.objects.get(pk=blogid)
        return redirect("publisherchange_blog",pk=post.id)
    else:
        return redirect("show_post")

def blog_view(request):
    blog_posts = Blog.objects.filter(is_approved=True)
    return render(request, 'blog.html', {'blog_posts': blog_posts})

@login_required
def editorgoup(request):
#     # Assign editor role to specific user
  
    if request.method=="POST":
        username = request.POST['name']
        editor_group, created = Group.objects.get_or_create(name="Editor")
        # user = User.objects.get(username=request.user)
        user = User.objects.get(username=username)
        user.groups.add(editor_group)
        return HttpResponse("Successfully Added into Group")
    else:
        return render(request,"editor.html")
from pytz import timezone as pytz_timezone
from datetime import datetime

def post(request,id):
    post = Blog.objects.get(pk=id)
    print(post.created_on)
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)

def detail(request,slug):
    post = Blog.objects.get(slug)

    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)

def cat_page(request,id):
    context_dict = {}
    category = Category.objects.get(pk=id)
    context_dict['category_name'] = category.Title

    pages = Blog.objects.filter(category=category)
    context_dict['pages'] = pages
    context_dict['category'] = category
    return render(request, 'category1.html', context_dict)

@login_required
def profile_update(request):
    if request.method == 'POST':
        p_form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        
        if p_form.is_valid():
            p_form.save()
            # messages.success(request,'Your Profile has been updated!')
            return redirect('blogpostapp:profile_update')
    else:
        p_form = UserUpdateForm(instance=request.user)
        
    context={
        'p_form': p_form,
        }
    return render(request, 'profile.html',context )

@login_required
def image_update(request):
    if request.method == 'POST':
        i_form = ImageupdateForm(request.POST,request.FILES,instance=request.user)
        
        if i_form.is_valid():
            i_form.save()
            # messages.success(request,'Your Profile has been updated!')
            return redirect('blogpostapp:viewuser')
    else:
        i_form= ImageupdateForm(instance=request.user)

    context={
        'i_form':i_form,
        }
    return render(request, 'image.html',context )

@login_required
def update_image(request,pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        image = request.FILES.get('file')
        if image:
            user.image = image
            user.save()
        return redirect('viewuser')

@login_required
def Add_comment(request, id):
    post = get_object_or_404(Blog, pk=id)
    # comments = Comment.objects.all()
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            body = request.POST.get('body')
            comment = Comment.objects.create(blog = post, user = request.user, body = body)
            comment.save()
            return redirect('blogpostapp:post', id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post,'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    b_id = comment.blog.pk
    print(b_id)
    post = get_object_or_404(Blog, pk=b_id)
    comments = Comment.objects.filter(blog=post)
    
    if comment.user == request.user:
        comment.delete()
        response_data = {
            'success': True,
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'success': False,
        }
    return JsonResponse(response_data)
    # return render(request, 'post_detail.html',{'comments': comments})
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            

@login_required
def reply_to_comment(request, comment_id):

    comment = Comment.objects.get(id=comment_id)
    blog=comment.blog
    if request.user != blog.author and not request.user.is_staff:
        return HttpResponseForbidden()

    reply_text = request.POST.get('reply_text')
    new_reply = Reply.objects.create(comment=comment, reply_text=reply_text)
    return redirect('blogpostapp:post', id=comment.blog.pk)

    # if request.method == 'POST':
    #     form = ReplyForm(request.POST)
    #     if form.is_valid():
    #         reply = form.save(commit=False)
    #         reply.comment = comment
    #         reply.author = request.user

    #         reply.save()
    #         return redirect('blogpostapp:post', id=comment.blog.pk)
    # else:
    #     form = ReplyForm()
    # return render(request, 'post_detail.html', {'form': form})
    
def comment_reply(request, id):
    # get post object
    # post = get_object_or_404(Blog, slug=post)
    post = get_object_or_404(Blog, pk=id)
    # list of active parent comments
    comments = post.comments.filter(active=True, parent_comment__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post = post
            # save
            new_comment.save()
            return redirect('blogpostapp:post', id=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': comment_form})

@login_required
def fav_postlist(request,id):
    user = get_object_or_404(User, pk=id)
    new = Blog.objects.filter(favourite=request.user)
    
    context = {
        'new': new,
    }
    return render(request, 'favourites.html',context)

@login_required
def favourite_add(request, id):
    post = get_object_or_404(Blog, pk=id)
    is_favorite = False
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
        is_favorite = True
    # return JsonResponse({'is_favorite': is_favorite})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def favorite_blog(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk)
    favorite = FavoriteBlog.objects.filter(user=user, blog=blog).first()
    if favorite:
        favorite.delete()
    else:
        FavoriteBlog.objects.create(user=user, blog=blog)
    return redirect('blogpostapp:fav_postlist', id=user.pk)

def CategoriesList(request):
    category = Category.objects.all()
    context={'category':category} 
    print(context)
    return render(request, "categories_list.html",context)

def toggle_heart(request):
        user = request.user
        id = request.POST.get('blog_id')
        post = get_object_or_404(Blog, pk=id)
        is_favorite = False
        if post.favourite.filter(id=request.user.id).exists():
            post.favourite.remove(request.user)
        else:
            post.favourite.add(request.user)
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite})

def add_comment(request):
    id = request.POST.get('blog_id')
    # add comment to database
    post = get_object_or_404(Blog, pk=id)
    comments = Comment.objects.filter(blog=post)
    comment_body = "False"
    if request.method == "POST":
        body = request.POST.get('body')
        print(body)
        comment = Comment.objects.create(blog = post, user = request.user, body = body)
        comment.save()
        comment_body = "True"
    return JsonResponse({"comment_body": comment_body,'comments':comments})

def update_comments(request):
    user = request.user
    id = request.POST.get('blog_id')
    post = get_object_or_404(Blog, pk=id)
    comments = Comment.objects.filter(blog=post)
    data = {'comments': comments}
    return JsonResponse(data)
    # return redirect('post_detail.html',{'comment': comments})
   
def refresh_comment(request, post_id):
    post = get_object_or_404(Blog, pk=post_id)
    comments = Comment.objects.filter(blog=post)
    data = {'comments': comments}
    # return JsonResponse(data)
    return JsonResponse({'comments': list(comments.values())})

class CommentList(generics.ListAPIView):
        # queryset = Comment.objects.all()
        serializer_class = Commentserializer
        pagination_class = Mycustompagination
        logging_methods = ['GET']

        def get_object(self):
            return get_object_or_404(Blog, id=self.request.query_params.get("post_id"))

        def get_queryset(self):
            post = get_object_or_404(Blog, id=self.kwargs['post_id'])
            return Comment.objects.filter(blog=post).order_by('-created')

class CommentPagination(CursorPagination):
    ordering = '-created'
    page_size = 2
    max_page_size=10
    
class CommentListAPIView(APIView):
    pagination_class = CommentPagination 

    def get(self, request,post_id,format=None):
        # post = get_object_or_404(Blog, pk=post_id)
        comments = Comment.objects.filter(blog_id=post_id)
        paginator = CommentPagination()
        result_page = paginator.paginate_queryset(comments,request)
        # return render(request, 'comments.html', {'comments': result_page})
        # return render(request, 'post_detail.html', {'comments': result_page})
        serializer = Commentserializer(result_page, many=True)
        print(serializer.data)
        return paginator.get_paginated_response(serializer.data)

def convert_time(request):
    # utc_datetime = datetime.now(tzutc())
    # local_timezone = pytz.timezone('Asia/Kolkata')
    # local_datetime = local_datetime.astimezone(local_timezone)
    # print(local_datetime)
    
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    tz = get_current_timezone()
    print('timezone: ' + str(tz))
    
    utc = datetime.now(tzutc())
    print('UTC TIME: ' + str(utc))

    local = utc.astimezone(tzlocal())
    print('Local TIME: ' + str(local))
    
    return JsonResponse({'utc': utc.isoformat(),'local':local})

def convert_to_localtime(utctime):

    print(utctime)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    utc = datetime.datetime.strptime(utctime,'%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())

    print(localtz.strftime(fmt))
    return localtz.strftime(fmt)

import json
def convert_utc_to_local(request):
    utcTime = request.GET.get('utc_time')
    print(utcTime)
    utc_datetime = datetime.strptime(utcTime, '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=pytz.utc)
    local_tz = pytz.timezone(timezone.get_current_timezone()) # Replace with your local timezone
    local_datetime = utc_datetime.astimezone(local_tz)
    response_data = {'local_time': local_datetime.strftime('%Y-%m-%d %H:%M:%S')}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

class BlogPagination(CursorPagination):
    ordering = '-created_on'
    page_size = 4
    max_page_size=50

class bloglist(generics.ListAPIView):
    # queryset = Blog.objects.all()
    model = Blog,Category
    serializer_class = BlogSerializer
    # template_name = ['template1.html', 'template2.html']
    # template_name = "blog.html"    
    
    def get(self, request,format=None):
        
        blogs=Blog.objects.filter(is_approved=True, is_published=True)
        paginator = BlogPagination()
        result_page = paginator.paginate_queryset(blogs,request)
        serializer = BlogSerializer(result_page, many=True)
        print(serializer.data)
        categories  = Category.objects.all()
        return paginator.get_paginated_response(serializer.data)
        # context = {'post': serializer.data,'categories':categories}
        # return render(request, 'blog.html', context)

        # return render(request, 'comments.html', {'comments': result_page})
        # return render(request, 'post_detail.html', {'comments': result_page})
        
