from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from .models import MeetUp

class LatestMeetUpTV(TemplateView):
    template_name = "past.html"

    def get_context_data(self, **kwargs):
        context = super(LatestMeetUpTV, self).get_context_data(**kwargs)
        context['latest'] = MeetUp.objects.order_by('-start_datetime')[:1]
        return context


def past_list(request):
    return render(request, 'pastlist.html')


def profile(request):
    return render(request, 'profile.html')


def speaker(request):
    return render(request, 'speaker.html')


def speaker_list(request):
    return render(request, 'speakerlist.html')


def schedule(request):
    return render(request, 'schedule.html')


def program(request):
    return render(request, 'program.html')


def registration(request):
    return render(request, 'registration.html')
