import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from meetup.models import MeetUp

User = get_user_model()


class Ticket(models.Model):
    """This model is a meet-up ticket for payment"""
    title = models.CharField(max_length=50)
    meet_up = models.ForeignKey(MeetUp)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    charge = models.PositiveIntegerField(default=0)
    maximum_count = models.PositiveIntegerField(default=0)
    start_time_to_sell = models.DateTimeField(default=timezone.now)
    sold_out_by_admin = models.BooleanField(default=True)
    is_main = models.BooleanField(default=True)
    refund_close_datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.refund_close_datetime = self.meet_up.start_datetime + datetime.timedelta(hours=-1)
        else:
            pass

        super(Ticket, self).save(*args, **kwargs)

    @property
    def is_sellable(self):
        if self.sold_out_by_admin:
            return False

        if self.not_yet_to_sell:
            return False

        if self.is_over_deadline:
            return False

        if self.is_over_maximum_count:
            return False

        return True

    @property
    def not_yet_to_sell(self):
        return timezone.now() < self.start_time_to_sell

    @property
    def is_over_deadline(self):
        return timezone.now() > self.meet_up.start_datetime

    @property
    def is_over_maximum_count(self):
        return Registration.objects.filter(ticket=self).count() >= self.maximum_count

    @property
    def is_refundable(self):
        return timezone.now() < self.refund_close_datetime


class Registration(models.Model):
    """This model is a registration for each meet-up with user
    and must be in transaction with PaymentHistory model"""
    user = models.ForeignKey(User, db_index=True)
    ticket = models.ForeignKey(Ticket)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_canceled = models.BooleanField(default=False, db_index=True)


class AttendCheck(models.Model):
    """This model is to check who attend"""
    registration = models.ForeignKey(Registration, db_index=True)
    is_attended = models.BooleanField(default=False)


class PaymentHistory(models.Model):
    """This model is to store payment history"""
    registration = models.OneToOneField(Registration, db_index=True)
    is_canceled = models.BooleanField(default=False)
    imp_uid = models.CharField(max_length=256, null=True)
    merchant_uid = models.CharField(max_length=256, null=True)

    # For extensibility
    payment_method_choices = (
        ('credit', 'Credit Card'),
        # ('transfer', 'Transfer'),
    )

    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
