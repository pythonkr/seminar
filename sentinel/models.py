from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from uuid import uuid4
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class EmailToken(models.Model):
    """This model is for token when someone sign in this website by email"""
    email = models.EmailField(verbose_name=_('The email was used to sign in'))
    token = models.UUIDField(default=uuid4, editable=False,
                             verbose_name=_('The token was generated by uuid'))
    created_at = models.DateTimeField(auto_now_add=True)


class EmailUserManager(BaseUserManager):
    def create_user(self, email):
        user = EmailUser.objects.create(email=email)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class EmailUser(AbstractBaseUser):
    email = models.EmailField(primary_key=True, verbose_name=_('email address'))
    is_admin = models.BooleanField(default=False)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

