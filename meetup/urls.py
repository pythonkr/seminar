from django.conf.urls import url

from .views import (
    LatestMeetUpTV,
    past_list, profile, program, ScheduleTemplateView, speaker, speaker_list, registration
)

urlpatterns = [
    url(r'^past/$', LatestMeetUpTV.as_view(), name='past'),
    url(r'^past_list/$', past_list, name='past_list'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^program/$', program, name='program'),
    url(r'^schedule/$', ScheduleTemplateView.as_view(), name='schedule'),
    url(r'^speaker/$', speaker, name='speaker'),
    url(r'^speaker_list/$', speaker_list, name='speaker_list'),
    url(r'^registration/$', registration, name='registration'),
]
