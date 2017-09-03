from django.test import TestCase


class ModelAttributeExistTest(TestCase):
    """This test class is for proving that the models' attributes exist between
    model what I declared on registration/models.py and model what I declared on other codes to use"""

    def test_ticket(self):
        """This test is for proving that the Ticket model's attributes exist"""
        from registration.models import Ticket
        from meetup.models import MeetUp, Venue

        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)

        self.fields_to_verify = ['title', 'meet_up', 'created_at', 'updated_at', 'charge', 'maximum_count',
                                 'start_time_to_sell', 'sold_out_by_admin']
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)
        self.ticket_fields = [field.name for field in self.ticket._meta.get_fields()]

        [self.assertIn(field, self.ticket_fields) for field in self.fields_to_verify]

    def test_registration(self):
        """This test is for proving that the Registration model's attributes exist"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)

        self.fields_to_verify = ['user', 'ticket', 'created_at', 'updated_at', 'is_canceled']
        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)
        self.registration_fields = [field.name for field in self.registration._meta.get_fields()]

        [self.assertIn(field, self.registration_fields) for field in self.fields_to_verify]

    def test_attend_check(self):
        """This test is for proving that the AttendCheck model's attributes exist"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration, AttendCheck
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)
        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)

        self.fields_to_verify = ['registration', 'is_attended']
        self.attend_check = AttendCheck.objects.create(registration=self.registration)
        self.attend_check_fields = [field.name for field in self.attend_check._meta.get_fields()]

        [self.assertIn(field, self.attend_check_fields) for field in self.fields_to_verify]

    def test_payment_history(self):
        """This test is for proving that the PaymentHistory model's attributes exist"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration, PaymentHistory
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)
        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)

        self.fields_to_verify = ['registration', 'is_canceled', 'payment_method']
        self.payment_history = PaymentHistory.objects.create(registration=self.registration,
                                                             payment_method=PaymentHistory.payment_method_choices[0][0])
        self.payment_history_fields = [field.name for field in self.payment_history._meta.get_fields()]

        [self.assertIn(field, self.payment_history_fields) for field in self.fields_to_verify]
