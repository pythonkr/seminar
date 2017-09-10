from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from meetup.models import MeetUp, Venue
from registration.models import Ticket, Registration

User = get_user_model()


class ModelMethodTest(TestCase):
    """This test class is for proving that the Ticket models' method operating well"""

    def test_ticket_is_sellable(self):
        """This test is for proving that the Ticket model's method `is_sellable() = True` operating well"""
        self.now = timezone.now()
        self.one_hour_later_from_now = self.now.replace(hour=self.now.hour + 1)
        self.two_hours_later_from_now = self.now.replace(hour=self.now.hour + 2)
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.sellable_meet_up = MeetUp.objects.create(title='This meet-up has sellable ticket', venue=self.venue,
                                                      start_datetime=self.one_hour_later_from_now,
                                                      end_datetime=self.two_hours_later_from_now)

        self.sellable_ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.sellable_meet_up, charge=10000,
                                                     maximum_count=10, start_time_to_sell=timezone.now(),
                                                     sold_out_by_admin=False)

        self.assertTrue(self.sellable_ticket.is_sellable())

    def test_ticket_is_not_sellable_by_admin(self):
        """This test is for proving that the Ticket model's method `is_sellable() = False` operating well by
        `sold_out_by_admin` attribute"""
        self.now = timezone.now()
        self.one_hour_later_from_now = self.now.replace(hour=self.now.hour + 1)
        self.two_hours_later_from_now = self.now.replace(hour=self.now.hour + 2)
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.not_sellable_meet_up = MeetUp.objects.create(title='This meet-up has not-sellable ticket',
                                                          venue=self.venue,
                                                          start_datetime=self.one_hour_later_from_now,
                                                          end_datetime=self.two_hours_later_from_now)

        self.not_sellable_ticket = Ticket.objects.create(title='Not Saleable Ticket', meet_up=self.not_sellable_meet_up,
                                                         charge=10000,
                                                         maximum_count=10, start_time_to_sell=timezone.now(),
                                                         sold_out_by_admin=True)

        self.assertFalse(self.not_sellable_ticket.is_sellable())
        self.assertTrue(self.not_sellable_ticket.sold_out_by_admin)

    def test_ticket_is_not_sellable_by_not_yet(self):
        """This test is for proving that the Ticket model's method `is_sellable() = False` and
        `not_yet_to_sell() = True` operating well"""
        self.now = timezone.now()
        self.half_hour_later_from_now = self.now.replace(minute=self.now.minute + 30)
        self.one_hour_later_from_now = self.now.replace(hour=self.now.hour + 1)
        self.two_hours_later_from_now = self.now.replace(hour=self.now.hour + 2)
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.not_sellable_meet_up = MeetUp.objects.create(title='This meet-up has not-sellable ticket',
                                                          venue=self.venue,
                                                          start_datetime=self.one_hour_later_from_now,
                                                          end_datetime=self.two_hours_later_from_now)

        self.not_sellable_ticket = Ticket.objects.create(title='Not Saleable Ticket', meet_up=self.not_sellable_meet_up,
                                                         charge=10000,
                                                         maximum_count=10,
                                                         start_time_to_sell=self.half_hour_later_from_now,
                                                         sold_out_by_admin=False)

        self.assertFalse(self.not_sellable_ticket.is_sellable())
        self.assertTrue(self.not_sellable_ticket.not_yet_to_sell())

    def test_ticket_is_not_sellable_by_over_deadline(self):
        """This test is for proving that the Ticket model's method `is_sellable() = False` and
       `is_over_deadline() = True` operating well"""
        self.now = timezone.now()
        self.one_hour_ago_from_now = self.now.replace(hour=self.now.hour - 1)
        self.two_hours_later_from_now = self.now.replace(hour=self.now.hour + 2)
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.not_sellable_meet_up = MeetUp.objects.create(title='This meet-up has not-sellable ticket',
                                                          venue=self.venue,
                                                          start_datetime=self.one_hour_ago_from_now,
                                                          end_datetime=self.two_hours_later_from_now)

        self.not_sellable_ticket = Ticket.objects.create(title='Not Saleable Ticket', meet_up=self.not_sellable_meet_up,
                                                         charge=10000,
                                                         maximum_count=10, start_time_to_sell=timezone.now(),
                                                         sold_out_by_admin=False)

        self.assertFalse(self.not_sellable_ticket.is_sellable())
        self.assertTrue(self.not_sellable_ticket.is_over_deadline())

    def test_ticket_is_not_sellable_by_over_maximum_count(self):
        """This test is for proving that the Ticket model's method `is_sellable() = False` and
       `is_over_maximum_count() = True` operating well"""
        self.now = timezone.now()
        self.one_hour_later_from_now = self.now.replace(hour=self.now.hour + 1)
        self.two_hours_later_from_now = self.now.replace(hour=self.now.hour + 2)
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.not_sellable_meet_up = MeetUp.objects.create(title='This meet-up has not-sellable ticket',
                                                          venue=self.venue,
                                                          start_datetime=self.one_hour_later_from_now,
                                                          end_datetime=self.two_hours_later_from_now)

        self.not_sellable_ticket = Ticket.objects.create(title='Not Saleable Ticket', meet_up=self.not_sellable_meet_up,
                                                         charge=10000,
                                                         maximum_count=1, start_time_to_sell=timezone.now(),
                                                         sold_out_by_admin=False)

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.registration = Registration.objects.create(user=self.user, ticket=self.not_sellable_ticket)

        self.assertFalse(self.not_sellable_ticket.is_sellable())
        self.assertTrue(self.not_sellable_ticket.is_over_maximum_count())
