from django.contrib import admin
from .models import *
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('Title','Desc','author','created_on','is_approved','is_published')
    list_filter = ('is_approved','is_published')
    search_fields = ['title', 'author']
    
admin.site.register(User)
admin.site.register(Blog,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(FavoriteBlog)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'blog', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name','body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
