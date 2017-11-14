from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Venue(models.Model):
    """This model is the venue where be held"""
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    map_link = models.URLField(max_length=255, null=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.location)


class ProgramCategory(models.Model):
    """This model is the category of program"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MeetUp(models.Model):
    """This model is to manage each meet-up"""
    title = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} : {}'.format(self.title, self.start_datetime.strftime("%Y년 %m월"))


class Profile(models.Model):
    """This model is which profile for user"""
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='username')
    organization = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='profile', null=True)
    biography = models.TextField(max_length=4000, null=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    """This model is lecture or event by speaker(s)"""
    # There should be difficulty and language information in Program?
    title = models.CharField(max_length=255)
    brief = models.TextField(null=True, verbose_name='simple information')
    description = models.TextField(null=True)
    speakers = models.ForeignKey(User, null=True)
    category = models.ForeignKey(ProgramCategory, null=True, verbose_name='The category which this program is belonged')
    slide_url = models.URLField(null=True, verbose_name='A slide url')
    pdf_url = models.URLField(null=True, verbose_name='A pdf url')
    video_url = models.URLField(null=True, verbose_name='A video url')
    is_recordable = models.BooleanField(default=True, verbose_name='recordable condition')
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)

    # If kind of session or lecture True, or not False (include breaktime)
    is_main_event = models.BooleanField(default=True, verbose_name='If kind of session or lecture True, or not False')
    meet_up = models.ForeignKey(MeetUp, null=True)
