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
from django.conf.urls import url
from django.contrib import admin

from meetup import views as meetup_view
from registration import views as registration_view

urlpatterns = [
    url(r'^$', meetup_view.index),
    url(r'^past/$', meetup_view.past),
    url(r'^past_list/$', meetup_view.past_list),
    url(r'^profile/$', meetup_view.profile),
    url(r'^program/$', meetup_view.program),
    url(r'^schedule/$', meetup_view.schedule),
    url(r'^speaker/$', meetup_view.speaker),
    url(r'^speaker_list/$', meetup_view.speaker_list),
    url(r'^coc/$', meetup_view.coc),

    url(r'^registration/$', registration_view.registration),

    url(r'^login/$', meetup_view.login),
    url(r'^mailsent/$', meetup_view.mailsent),

    url(r'^admin/', admin.site.urls)
]
