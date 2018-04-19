from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
    path('TweetUtils/', include('TweetUtils.urls')),
    path('admin/', admin.site.urls),
    path('',RedirectView.as_view(url='/TweetUtils/')),
    url('^', include('django.contrib.auth.urls')),
]
