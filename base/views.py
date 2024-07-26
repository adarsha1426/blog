from typing import Any
from django.shortcuts import render,redirect
from django.http import Http404
from .models import Post , Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout as auth_logout
from .forms import EmailPostForm,RegistrationForm,LoginForm,CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count
from django.contrib import messages
#class based views
from django.views.generic import ListView

# Create your views here.
def home(request):
    user=request.user
    return render(request,'base/post/home.html')
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')  
            else:
                messages.error(request,"Invalid Login Credntial")
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'base/registration/login.html', {'form': form})

def logout_view(request):
    messages.success(request,"You have been successfully loggd out")
    auth_logout(request)
    return redirect('base:login')

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created")
            return redirect('/login')
    else:
        form=RegistrationForm()
    return render(request,'base/registration/sign_up.html',{'form':form})


def get_context():
    context = {}
    context['high_comment'] = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    return context
def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)  # Show 3 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
    }
    custom_context = get_context()
    context.update(custom_context)
    
    return render(request, 'base/post/list.html', context)

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    if request.method=="POST":
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
        else:
            form=EmailPostForm()
    return render(request,'post/share.html',{'post':post,'form':form})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,
                  'base/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user=request.user
        comment.post = post
        comment.save()
    return render(request, 'base/post/comment.html',
                           {'post': post,
                            'comment_form': form,
                            'comment': comment})

def email(request):
    email_form=EmailPostForm()
    if request.method=="POST":
        form=EmailPostForm(request.post)
        if form.is_valid():
            name=form.cleaned_data('name')
            email=form.cleaned_data('email')
            to=form.cleaned_data('to')
            comments=form.cleaned_data('comments')
            send_mail(
                        "Subject",
                        "Message",
                        "adarshamishra89@gmail.com",
                        ['adarshamishra98@gmail.com'],
                    )
            print(name,email,to,email,comments)
            form.save()
    else:
        email_form=EmailPostForm()
        return render(request,"base/post/email_form.html",{'email_form':email_form})
