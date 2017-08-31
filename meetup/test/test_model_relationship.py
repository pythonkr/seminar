from django.test import TestCase


class ModelRelationshipTestCase(TestCase):
    """This test class is for proving that the relationship among declared django models are organized successfully"""

    def test_user_has_the_profile(self):
        """This test is for proving that a user has a profile"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from meetup.models import Profile
        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.profile = Profile.objects.create(user=self.user, name='Noh Seho',
                                              slug='seho', organization='PyCon Korea')

        self.assertEqual(self.profile.user.username, 'username')
        self.assertEqual(self.user.profile.slug, 'seho')

    def test_user_become_a_speaker(self):
        """This test is for proving that a user become a speaker"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from meetup.models import Speaker
        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.speaker = Speaker.objects.create(user=self.user)

        self.assertEqual(self.speaker.user.username, 'username')

    def test_program_has_a_program_category(self):
        """This test is for proving that a program has a program category"""
        from meetup.models import Program, ProgramCategory
        self.program_category = ProgramCategory.objects.create(name='Ruby', slug='ruby')
        self.program = Program.objects.create(title='How to migrate from ruby to python',
                                              brief='Have you ever write down the ruby code?',
                                              description='Then you should watch this program',
                                              category=self.program_category)

        self.assertEqual(self.program.category.name, 'Ruby')

    def test_speaker_has_a_program(self):
        """This test is for proving that a speaker has a program"""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from meetup.models import Speaker, Program
        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.speaker = Speaker.objects.create(user=self.user)
        self.program = Program.objects.create(title='How to migrate from ruby to python',
                                              brief='Have you ever write down the ruby code?',
                                              description='Then you should watch this program')
        self.program.speakers.add(self.speaker)

        self.assertEqual(self.program.speakers.count(), 1)

    def test_venue_is_valid(self):
        """This test is for proving that the venue information including lat, lon is correctly saved"""
        from meetup.models import Venue
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)

        self.assertEqual(self.venue.name, 'Seoul City Hall')
        self.assertEqual(self.venue.latitude, 37.566676)
        self.assertEqual(self.venue.longitude, 126.978397)
