"""Pydate URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from Pydate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base,),
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('chat/', include('Chat.urls')),
    path('profile/', views.profile),
    path('help/',views.info_view, name='info'),
    path('profile/edit/', views.update_profile),
    path('<str:username>/personal_questionnaire/', views.personal_questionnaire, name="personal_questionnaire"),
    path('my_matches/', views.my_matches, name="my_matches"),
    path('view_answers/', views.view_answers, name="view_answers"),
    path('view_people/', views.view_people, name="view_people"),
    url(r'^view_answers/(?P<id>\d+)/delete_match$', views.match_delete, name='match_delete'),
    url(r'^view_answers/(?P<id>\d+)/accept_match$', views.match_accept, name='match_accept'),
    url(r'^view_people/(?P<id>\d+)/make_crush$', views.yes_crush, name='yes_crush'),
    url(r'^view_people/(?P<id>\d+)/decline_crush$', views.no_crush, name='no_crush'),


    url(r'^logout/$', views.logout_view, name='logout')
]
from django.conf import settings

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
