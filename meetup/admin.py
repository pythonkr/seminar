from django.contrib import admin

from .models import Venue, ProgramCategory, MeetUp, Program, Profile

admin.site.register(Venue)
admin.site.register(MeetUp)


@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'brief', 'meet_up',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
