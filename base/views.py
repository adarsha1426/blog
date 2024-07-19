from django.shortcuts import render,redirect
from django.http import Http404
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout as auth_logout
from .forms import EmailPostForm,RegistrationForm,LoginForm,CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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
                return redirect('/home')  # Redirect to the home page after successful login
            else:
                # Invalid login credentials
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'base/registration/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('base:login')

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form=RegistrationForm()
    return render(request,'base/registration/sign_up.html',{'form':form})


class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='base/post/list.html'


def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    if request.method=="POST":
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
        else:
            form=EmailPostForm()
    return render(request,'base/post/share.html',{'post':post,'form':form})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request,
                  'base/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
        return render(request,'base/post/comment.html',{
                                            'post':post,
                                                'form':form,
                                                'comment':comment
                                                 })
    else:
        form=CommentForm()
        print(form.label_suffix)
    return render(request,'blog/post/comment_form.html',{'post':post,
                                                        'comment':comment,
                                                        'form':form})

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


















# def post_list(request):
#     post_list = Post.published.all()
#     # Pagination with 3 posts per page
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts=paginator.page(page_number)
#     except PageNotAnInteger:
#         #if page is not an integer
#         posts=paginator.page(1)
#     except EmptyPage:
#         #if page number is out of range deliver last page of results
#         posts=paginator.page(paginator.num_pages)
#     return render(request,
#                   'base/post/list.html',
#                   {'posts': posts})