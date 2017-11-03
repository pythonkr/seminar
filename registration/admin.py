from django.contrib import admin

from .models import Ticket, Registration, AttendCheck, PaymentHistory


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'meet_up', 'charge', 'maximum_count', 'start_time_to_sell', 'sold_out_by_admin',
                    'is_main', 'refund_close_datetime',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at', 'updated_at', 'is_canceled',)


@admin.register(AttendCheck)
class AttendCheckAdmin(admin.ModelAdmin):
    list_display = ('registration', 'is_attended',)


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('registration', 'is_canceled', 'payment_method',)
