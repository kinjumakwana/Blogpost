from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as authentication_view
from .views import *
app_name = "blogpostapp"

urlpatterns = [
    path('', index, name="index"),
    path('SignUp/',SignUp.as_view(), name="SignUp"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',authentication_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('editorgoup/',editorgoup, name="editorgoup"),
    path('author_group/',author_group, name="author_group"),
    path('publisher_group/',publisher_group, name="publisher_group"),
    path('viewuser/',viewuser, name="viewuser"),
    path('show_post/',show_post, name="show_post"),
    path('blog/',blog, name="blog"),
    path('contact/',contact, name="contact"),
    path('about/',about, name="about"),

    path('create_blog/',create_blog, name="create_blog"),
    path('create_category/',create_category, name="create_category"),
    path('delete/<int:blog_id>/',delete_blog, name='delete_blog'),
    path('profile_update/',profile_update, name='profile_update'),
    path('image_update/',image_update, name='image_update'),
    path('update_image/<int:pk>', update_image, name='update_image'),
    
    path('authorchange_blog/<int:id>',authorchange_blog, name="authorchange_blog"),
    path('editorchange_blog/<int:id>',editorchange_blog, name="editorchange_blog"),
    path('publisherchange_blog/<int:id>',publisherchange_blog, name="publisherchange_blog"),
    path('masterchange_blog/',masterchange_blog, name="masterchange_blog"),
    
    path('post/<int:id>',post,name="post"),
    
    path('blogdetial/',blogdetial, name="blogdetial"),
    path('checkgroup/',check_user_in_group, name="checkgroup"),
    
    # path('<slug:slug>/',detail, name="detail"),
    path('cat_page/<int:id>',cat_page, name="cat_page"),

    path('Add_comment/<int:id>',Add_comment, name="Add_comment"),
    # path('delete_comment/<int:comment_id>',delete_comment, name="delete_comment"),
    # path('delete_comment/',delete_comment, name="delete_comment"),
    path('delete/<int:pk>', delete_comment, name='delete'),
    path('reply_to_comment/<int:comment_id>/',reply_to_comment, name='reply_to_comment'),
    path('comment_reply/<int:id>/',comment_reply, name='comment_reply'),

   path('gpermission/',create_group_permission, name="gpermission"),
   path('fav_postlist/<int:id>/',fav_postlist, name="fav_postlist"),
   path('favourite_add/<int:id>/',favourite_add, name="favourite_add"),
   path('favorite/<int:pk>',favorite_blog, name='favorite_blog'),
   path('CategoriesList',CategoriesList, name='CategoriesList'),
   path('toggle_heart', toggle_heart, name='toggle_heart'),
   path("add_comment/", add_comment, name="add_comment"),
   path("update_comments/", update_comments, name="update_comments"),
   path("refresh_comment/<int:post_id>/", refresh_comment, name="refresh_comment"),
   path('commentpag/<int:post_id>/', CommentList.as_view(), name='commentpag'),
   path('comments/<int:post_id>/', CommentListAPIView.as_view(), name='comments'),
#    path('blog_post_detail/<int:pk>/', blog_post_detail, name='blog_post_detail'),
#    path('load_comments/<int:post_id>/', load_comments, name='load_comments'),
#    path('comments/<int:post_id>/', CommentListView, name='comment_list'),
#    path('comments/<int:blog_id>/', load_comments, name='load_comments'),
    # path('load/', load_more, name='load')
    # path('get_offset/', get_offset, name='get_offset'),
    # path('get_utc_time/', get_utc_time, name='get_utc_time'),
    path('convert_time/', convert_time, name='convert_time'),
    path('bloglist/', bloglist.as_view(), name='bloglist'),
    path('convert_utc_to_local/', convert_utc_to_local, name='convert_utc_to_local'),
    path('convert_to_localtime/<str:utctime>/', convert_to_localtime, name='convert_to_localtime'),

    
]
