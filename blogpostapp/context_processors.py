from .models import *

def categories(request):
    return {'categories': Category.objects.all()}

def comments(request):
    comments = Comment.objects.all()
    return {'comments': comments}