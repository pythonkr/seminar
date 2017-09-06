from django.test import TestCase


class ModelAttributeExistTest(TestCase):
    """This test class is for proving that the models' attributes exist between
    model what I declared on meetup/models.py and model what I declared on other codes to use"""

    def test_profile(self):
        """This test is for proving that the Profile model's attributes exist"""
        from django.contrib.auth import get_user_model
        from meetup.models import Profile
        User = get_user_model()

        self.fields_to_verify = ['user', 'name', 'slug', 'organization', 'image', 'biography']
        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.profile = Profile.objects.create(user=self.user, name='Noh Seho',
                                              slug='seho', organization='PyCon Korea')

        self.profile_fields = [field.name for field in self.profile._meta.get_fields()]

        [self.assertIn(field, self.profile_fields) for field in self.fields_to_verify]

    def test_email_token(self):
        """This test is for proving that the EmailToken model's attributes exist"""
        from meetup.models import EmailToken

        self.fields_to_verify = ['email', 'token', 'created_at']
        self.email_token = EmailToken.objects.create(email='test@email.com')

        self.email_token_fields = [field.name for field in self.email_token._meta.get_fields()]

        [self.assertIn(field, self.email_token_fields) for field in self.fields_to_verify]

    def test_venue(self):
        """This test is for proving that the Venue model's attributes exist """
        from meetup.models import Venue

        self.fields_to_verify = ['name', 'location', 'description', 'latitude', 'longitude']
        self.venue = Venue.objects.create(name='Seoul City Hall', location='Seoul', latitude=37.566676,
                                          longitude=126.978397)

        self.venue_fields = [field.name for field in self.venue._meta.get_fields()]

        [self.assertIn(field, self.venue_fields) for field in self.fields_to_verify]

    def test_program_category(self):
        """This test is for proving that the ProgramCategory model's attributes exist"""
        from meetup.models import ProgramCategory

        self.fields_to_verify = ['name', 'slug']
        self.program_category = ProgramCategory.objects.create(name='Ruby', slug='ruby')

        self.program_category_fields = [field.name for field in self.program_category._meta.get_fields()]

        [self.assertIn(field, self.program_category_fields) for field in self.fields_to_verify]

    def test_speaker(self):
        """This test is for proving that the Speaker model's attributes exist"""
        from django.contrib.auth import get_user_model
        from meetup.models import Speaker
        User = get_user_model()

        self.fields_to_verify = ['user']
        self.user = User.objects.create_user('username', 'test@email.com', 'password')
        self.speaker = Speaker.objects.create(user=self.user)

        self.speaker_fields = [field.name for field in self.speaker._meta.get_fields()]

        [self.assertIn(field, self.speaker_fields) for field in self.fields_to_verify]

    def test_program(self):
        """This test is for proving that the Program model's attributes exist"""
        from meetup.models import Program, ProgramCategory

        self.fields_to_verify = ['title', 'brief', 'description', 'speakers', 'category', 'slide_url', 'pdf_url',
                                 'video_url', 'is_recordable', 'is_main_event']
        self.program_category = ProgramCategory.objects.create(name='Ruby', slug='ruby')
        self.program = Program.objects.create(title='How to migrate from ruby to python',
                                              brief='Have you ever write down the ruby code?',
                                              description='Then you should watch this program',
                                              category=self.program_category)

        self.program_fields = [field.name for field in self.program._meta.get_fields()]

        [self.assertIn(field, self.program_fields) for field in self.fields_to_verify]

    def test_meet_up(self):
        """This test is for proving that the MeetUp model's attributes exist"""
        from meetup.models import Venue, MeetUp

        self.fields_to_verify = ['title', 'venue', 'start_datetime', 'end_datetime']
        self.venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        self.meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=self.venue)

        self.meet_up_fields = [field.name for field in self.meet_up._meta.get_fields()]

        [self.assertIn(field, self.meet_up_fields) for field in self.fields_to_verify]
