"""seminar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import IndexView, CocTV

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^coc/$', CocTV.as_view(), name='coc'),

    url(r'^admin/', admin.site.urls),
    url(r'^sentinel/', include('sentinel.urls', namespace='sentinel')),
    url(r'^meetup/', include('meetup.urls', namespace='meetup')),
    url(r'^payment/', include('registration.urls', namespace='payment')),
]
