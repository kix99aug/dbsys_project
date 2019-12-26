"""DBproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from COMPARE import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('mylinebot/', include('mylinebot.urls')),

    path('search', views.search),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('comment', views.comment),
    path('api/login', views.api_login),
    path('api/register', views.api_register),
    path('api/search', views.api_search),
    path('api/comment/add', views.api_comment_add),
    path('api/comment/update', views.api_comment_update),
    path('api/comment/delete', views.api_comment_delete),
    path('github/callback',views.github_callback),
    path('', include('social_django.urls', namespace='social'))

    path('accounts',include('allauth.urls')),
]
