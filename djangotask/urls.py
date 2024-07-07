"""
URL configuration for djangotask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,re_path
from Registerapp import views
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.homepage),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('create_user/', views.create_user, name='create_user'),
    path('list/', views.profile_list,name='profile_list'),
    path('delete/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('edit/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_out, name='login'),
    path('blog_create/', views.blog_create, name='blog_create'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('edit-blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    
    # path('register/', views.register_user, name='register_user'),
    
    #  re_path(r'^api/uploadjson',file_view.upload_insight),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
