from django.conf.urls import url

from .views import past, past_list, profile, program, schedule, speaker, speaker_list, registration

urlpatterns = [
    url(r'^past/$', past, name='past'),
    url(r'^past_list/$', past_list, name='past_list'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^program/$', program, name='program'),
    url(r'^schedule/$', schedule, name='schedule'),
    url(r'^speaker/$', speaker, name='speaker'),
    url(r'^speaker_list/$', speaker_list, name='speaker_list'),
    url(r'^registration/$', registration, name='registration'),
]
