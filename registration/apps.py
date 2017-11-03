import logging

from django.apps import AppConfig

logger = logging.getLogger('registration')


class RegistrationConfig(AppConfig):
    name = 'registration'
