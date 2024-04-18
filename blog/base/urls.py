from django.urls import path
from . import views

app_name='base'
urlpatterns = [
    path('home',views.home,name='home'),
    path('list',views.post_list,name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
]
