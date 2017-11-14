from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic.base import TemplateView

from meetup.models import MeetUp
from registration.models import Ticket


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        now_meet_up = MeetUp.objects.last()
        context['now_meet_up'] = now_meet_up
        context['last_meet_ups'] = MeetUp.objects.all()

        d_day = timezone.now() - now_meet_up.start_datetime
        d_day = d_day.days

        if d_day == 0:
            d_day = 'D-Day'
        elif d_day > 0:
            d_day = 'D+{}'.format(d_day)
        elif d_day < 0:
            d_day = 'D{}'.format(d_day)
        else:
            d_day = '준비중입니다.'

        context['d_day'] = d_day

        try:
            now_ticket = Ticket.objects.filter(is_main=True).get(meet_up=now_meet_up)
            context['now_ticket'] = now_ticket
        except ObjectDoesNotExist as exception:
            pass

        try:
            now_programs = now_meet_up.program_set.all()
            context['now_programs'] = now_programs
        except ObjectDoesNotExist as exception:
            pass

        return context


class CocTV(TemplateView):
    template_name = 'coc.html'
