from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from meetup.models import MeetUp

User = get_user_model()


class Ticket(models.Model):
    """This model is a meet-up ticket for payment"""
    title = models.CharField(max_length=50)
    meet_up = models.OneToOneField(MeetUp)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    charge = models.PositiveIntegerField(default=0)
    maximum_count = models.PositiveIntegerField(default=0)
    start_time_to_sell = models.DateTimeField(default=timezone.now)
    sold_out_by_admin = models.BooleanField(default=True)

    def is_sellable_this_ticket(self):
        if self.sold_out_by_admin:
            return False

        if self.not_yet_to_sell():
            return False

        if self.is_over_deadline():
            return False

        if self.is_over_maximum_count():
            return False

        return True

    def not_yet_to_sell(self):
        return timezone.now() < self.start_time_to_sell

    def is_over_deadline(self):
        return timezone.now() > self.meet_up.start_datetime

    def is_over_maximum_count(self):
        return Registration.objects.filter(ticket=self).count() >= self.maximum_count


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
    registration = models.ForeignKey(Registration, db_index=True)
    is_canceled = models.BooleanField(default=False)

    # For extensibility
    payment_method_choices = (
        ('credit', 'Credit Card'),
        # ('transfer', 'Transfer'),
    )

    payment_method = models.CharField(max_length=10, choices=payment_method_choices)
