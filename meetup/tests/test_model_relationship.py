from django.contrib.auth import get_user_model
from django.test import TestCase

from meetup.models import Profile, Program, ProgramCategory, Venue, MeetUp

User = get_user_model()


class ModelRelationshipTestCase(TestCase):
    """This test class is for proving that the relationship among declared django models are organized successfully"""

    def test_user_has_the_profile(self):
        """This test is for proving that a user has a profile"""
        self.user = User.objects.create_user('test@email.com')
        self.profile = Profile.objects.create(user=self.user, name='Noh Seho',
                                              slug='seho', organization='PyCon Korea')

        self.assertEqual(self.profile.user.email, 'test@email.com')
        self.assertEqual(self.user.profile.slug, 'seho')

    def test_program_has_a_program_category(self):
        """This test is for proving that a program has a program category"""
        self.program_category = ProgramCategory.objects.create(name='Ruby', slug='ruby')
        self.program = Program.objects.create(title='How to migrate from ruby to python',
                                              brief='Have you ever write down the ruby code?',
                                              description='Then you should watch this program',
                                              category=self.program_category)

        self.assertEqual(self.program.category.name, 'Ruby')

    def test_speaker_has_a_program(self):
        """This test is for proving that a speaker has a program"""
        self.user = User.objects.create_user('test@email.com')
        self.program = Program.objects.create(title='How to migrate from ruby to python',
                                              brief='Have you ever write down the ruby code?',
                                              description='Then you should watch this program',
                                              speakers=self.user)

        self.assertEqual(self.program.speakers, self.user)

    def test_venue_is_valid(self):
        """This test is for proving that the venue information including lat, lon is correctly saved"""
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.assertEqual(self.venue.name, 'Seoul City Hall')
        self.assertEqual(self.venue.latitude, 37.566676)
        self.assertEqual(self.venue.longitude, 126.978397)

    def test_meet_up_has_venue(self):
        """This test is for proving that a meet-up has a venue"""
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)

        self.assertEqual(self.meet_up.venue.name, 'Seoul City Hall')
        self.assertEqual(self.venue.meetup_set.get(id=self.meet_up.id).title, 'Python User Group Bimonthly Seminar')
