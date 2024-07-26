from django.urls import path
from . import views



app_name='base'
urlpatterns = [
    path('',views.post_list,name='home'),
    path('home',views.post_list,name='home'),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),
    path('register',views.register,name="register"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('comment/<int:post_id>',views.post_comment,name='add_comment'),
    path('email',views.email,name="email"),


]   
