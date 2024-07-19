from django.urls import path
from . import views
from .views import PostListView


app_name='base'
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('register',views.register,name="register"),
    path('list',PostListView.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
     path('<int:post_id>/comment',views.post_comment,name='add_comment'),
    path('email',views.email,name="email"),
    
]
