from django.urls import path
from django.conf.urls import url
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('user/create/' , views.create_user),
    path('user/login/', views.user_login),
    path('user/logout/', views.user_logout),
    path('addlocation/', views.addlocation),
    path('deletecity/',views.deletecity),
    path('sendmail/',views.sendmail),
    url(r'^password_reset/$', auth_views.password_reset),
    url(r'^password_reset/done/$', auth_views.password_reset_done),
]
