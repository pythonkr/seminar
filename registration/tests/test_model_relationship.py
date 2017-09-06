from django.test import TestCase


class ModelRelationshipTestCase(TestCase):
    """This test class is for proving that the relationship among declared django models are organized successfully"""

    def test_ticket_has_the_meet_up(self):
        """This test is for proving that a ticket has one meet-up"""

        from registration.models import Ticket
        from meetup.models import MeetUp, Venue

        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)

        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)

        self.assertEqual(self.ticket.title, 'Normal Ticket')
        self.assertEqual(self.ticket.meet_up.title, 'Python User Group Bimonthly Seminar')
        self.assertEqual(self.ticket.meet_up.venue.name, 'Seoul City Hall')

    def test_registration_has_the_ticket_and_the_user(self):
        """This test is for proving that a registration has the ticket and the user"""

        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)

        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)

        self.assertEqual(self.registration.user.username, 'username')
        self.assertEqual(self.registration.ticket.title, 'Normal Ticket')

    def test_attend_check_has_the_registration(self):
        """This test is for proving that a attend check has the registration"""

        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration, AttendCheck
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)
        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)

        self.attend_check = AttendCheck.objects.create(registration=self.registration)

        self.assertIsNotNone(self.attend_check.registration)

    def test_payment_history_has_the_registration(self):
        """This test is for proving that a payment history has the registration"""

        from django.contrib.auth import get_user_model
        User = get_user_model()

        from registration.models import Ticket, Registration, PaymentHistory
        from meetup.models import MeetUp, Venue

        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)
        self.ticket = Ticket.objects.create(title='Normal Ticket', meet_up=self.meet_up, charge=10000)
        self.registration = Registration.objects.create(user=self.user, ticket=self.ticket)

        self.payment_history = PaymentHistory.objects.create(registration=self.registration,
                                                             payment_method=PaymentHistory.payment_method_choices[0][0])

        self.assertIsNotNone(self.payment_history.registration)
        self.assertEqual(self.payment_history.payment_method, 'credit')
