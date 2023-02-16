from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login_view, name='login'),
    path('logout/', views.Logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('home/<int:id>/', views.home, name='home'),
    re_path(r'article/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$', views.article, name= 'article')
]
