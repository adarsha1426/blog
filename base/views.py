from django.shortcuts import render
from django.http import Http404
from .models import Post
# Create your views here.
def home(request):
    return render(request,'base/post/home.html')

def post_list(request):
    posts=Post.published.all()
    return render(request,'base/post/list.html',{'posts':posts})

def post_detail(request,id):
    try:
        post=Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found")

    return render(request,'base/post/detail.html',{'post':post})
