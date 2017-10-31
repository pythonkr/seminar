from constance import config
from django.contrib.auth import get_user_model
from django.utils import timezone
from iamport import Iamport

from .apps import logger
from .models import Ticket, Registration, AttendCheck, PaymentHistory

User = get_user_model()


# TODO: Log all transaction after logger setting done

def _process_exception(exception: Exception):
    if isinstance(exception, Iamport.ResponseError):
        return False, exception.message,
    else:
        return False, str(exception),


def _payment_process_for_domestic(**payload):
    """Process payment via Iamport PG service
    For domestic, ['merchant_uid', 'amount', 'card_number', 'expiry', 'birth', 'pwd_2digit']"""
    iamport = Iamport(config.IAMPORT_API_KEY_FOR_DOMESTIC, config.IAMPORT_API_SECRET_FOR_DOMESTIC)

    try:
        result = iamport.pay_onetime(**payload)
        return True, result,
    except Exception as exception:
        return _process_exception(exception)


def _payment_process_for_international(**payload):
    """Process payment via Iamport PG service
    For international, ['merchant_uid', 'amount', 'card_number', 'expiry']:"""
    iamport = Iamport(config.IAMPORT_API_KEY_FOR_INTERNATIONAL, config.IAMPORT_API_SECRET_FOR_INTERNATIONAL)

    try:
        result = iamport.pay_foreign(**payload)
        return True, result,
    except Exception as exception:
        return _process_exception(exception)


def _cancel_process_for_domestic(**payload):
    """Process a cancel request by imp_uid"""
    iamport = Iamport(config.IAMPORT_API_KEY_FOR_DOMESTIC, config.IAMPORT_API_SECRET_FOR_DOMESTIC)

    try:
        result = iamport.cancel_by_imp_uid(**payload)
        return True, result,
    except Exception as exception:
        return _process_exception(exception)


def _cancel_process_for_international(**payload):
    """Process a cancel request by imp_uid"""
    iamport = Iamport(config.IAMPORT_API_KEY_FOR_INTERNATIONAL, config.IAMPORT_API_SECRET_FOR_INTERNATIONAL)

    try:
        result = iamport.cancel_by_imp_uid(**payload)
        return True, result,
    except Exception as exception:
        return _process_exception(exception)


def _payment_process(for_domestic: bool, **payload):
    if for_domestic:
        return _payment_process_for_domestic(**payload)
    else:
        return _payment_process_for_international(**payload)


def _cancel_process(for_domestic: bool, **payload):
    if for_domestic:
        return _cancel_process_for_domestic(**payload)
    else:
        return _cancel_process_for_international(**payload)


class Counter(object):
    @classmethod
    def buy_ticket(cls, ticket: Ticket, user: User,
                   buyer_name: str, card_number: str, expiry: str,
                   amount: int, for_domestic: bool,
                   birth: str = None, pwd_2digit: str = None):
        """Buy a ticket"""
        payload = {
            'name': ticket.title,
            'email': user.email,
            'buyer_name': buyer_name,
            'buyer_email': user.email,
            'amount': amount,
            'card_number': card_number,
            'expiry': expiry,
            'merchant_uid': '{}_{}_{}'.format(ticket.title,
                                              buyer_name,
                                              '{:.0f}'.format(timezone.now().utcnow().timestamp())),
        }

        if for_domestic:
            payload['birth'] = birth
            payload['pwd_2digit'] = pwd_2digit

        is_success, result = _payment_process(for_domestic, **payload)

        if not is_success:
            logger.error('User "%s" failed buying the "%s" ticket, because of "%s"',
                         user.email,
                         ticket.title,
                         result,
                         )
            return False

        try:
            registration = Registration.objects.create(user=user, ticket=ticket)
            attend_check = AttendCheck.objects.create(registration=registration)
            payment_history = PaymentHistory.objects.create(registration=registration, imp_uid=result['imp_uid'],
                                                            merchant_uid=payload['merchant_uid'],
                                                            # Temporary only credit card
                                                            payment_method=PaymentHistory.payment_method_choices[0][0])

            registration.save()
            attend_check.save()
            payment_history.save()

            return True
        except Exception as exception:
            logger.error('User "%s" failed registration, because of "%s"',
                         user.email,
                         str(exception),
                         )
            return False

    @classmethod
    def validate_payment_transaction(cls):
        """This method will be a checking the validation of payment transaction"""
        pass

    @classmethod
    def cancel_registration(cls, registration: Registration, for_domestic: bool):
        """Cancel a registration"""
        payment_history = PaymentHistory.objects.filter(registration=registration).get()
        payload = {
            'imp_uid': payment_history.imp_uid,
            'reason': None,
        }

        is_success, result = _cancel_process(for_domestic, **payload)

        if not is_success:
            logger.error('User "%s" failed cancel payment, because of "%s"',
                         registration.user.email,
                         result,
                         )
            return False

        try:
            payment_history.is_canceled = True
            registration.is_canceled = True

            payment_history.save()
            registration.save()

            return True
        except Exception as exception:
            logger.error('User "%s" failed cancel registration, because of "%s"',
                         registration.user.email,
                         str(exception),
                         )
            return False
