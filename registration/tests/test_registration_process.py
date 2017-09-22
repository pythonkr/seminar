import requests_mock
from django.contrib.auth import get_user_model
from django.test import TestCase

from meetup.models import Venue, MeetUp
from ..counter import Counter
from ..models import Ticket, Registration, AttendCheck, PaymentHistory

User = get_user_model()


class RegistrationProcessTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('test@email.com')
        venue = Venue.objects.create(name='Seoul City Hall', latitude=37.566676, longitude=126.978397)
        meet_up = MeetUp.objects.create(title='Python User Group Bimonthly Seminar', venue=venue)
        ticket = Ticket.objects.create(title='Test Ticket', meet_up=meet_up, charge=10000)

        user.save()
        venue.save()
        meet_up.save()
        ticket.save()

    @requests_mock.mock()
    def test_buy_a_ticket_domestic(self, mock_server):
        # MOCK DATA for get token and pay
        mock_server.post('https://api.iamport.kr/users/getToken',
                         json={"code": 0,
                               "message": None,
                               "response":
                                   {
                                       "access_token": "ANONYMOUS TOKEN",
                                       "now": 1508000158,
                                       "expired_at": 1508001239}
                               })
        mock_server.post('https://api.iamport.kr/subscribe/payments/onetime',
                         json={"code": 0,
                               "message": None,
                               "response":
                                   {"amount": 1000,
                                    "apply_num": "09249488",
                                    "bank_code": None,
                                    "bank_name": None,
                                    "buyer_addr": None,
                                    "buyer_email": "test@email.com",
                                    "buyer_name": "Test Buyer Name",
                                    "buyer_postcode": None,
                                    "buyer_tel": None,
                                    "cancel_amount": 0,
                                    "cancel_history": [],
                                    "cancel_reason": None,
                                    "cancel_receipt_urls": [],
                                    "cancelled_at": 0,
                                    "card_code": "361",
                                    "card_name": "BC\uce74\ub4dc",
                                    "card_quota": 0,
                                    "cash_receipt_issued": False,
                                    "currency": "KRW",
                                    "custom_data": None,
                                    "escrow": False,
                                    "fail_reason": None,
                                    "failed_at": 0,
                                    "imp_uid": "imps_824159804810",
                                    "merchant_uid": "Test Ticket_Test Buyer Name_1507967757",
                                    "name": "Test Ticket",
                                    "paid_at": 1508000159,
                                    "pay_method": "card",
                                    "pg_provider": "jtnet",
                                    "pg_tid": "tpaytest7m01241710150155598237",
                                    "receipt_url": "https:\/\/www.tpay.co.kr\/issue\/ChkIssueLoader.jsp"
                                                   "?TID=tpaytest7m01241710150155598237&type=0",
                                    "status": "paid",
                                    "user_agent": "sorry_not_supported_anymore",
                                    "vbank_code": None,
                                    "vbank_date": 0,
                                    "vbank_holder": None,
                                    "vbank_name": None,
                                    "vbank_num": None}
                               })

        user = User.objects.get(email='test@email.com')
        venue = Venue.objects.get(name='Seoul City Hall')
        meet_up = MeetUp.objects.get(venue=venue)
        ticket = Ticket.objects.get(meet_up=meet_up)

        # TODO: Insert that values
        is_success = Counter.buy_ticket(ticket=ticket,
                                        user=user,
                                        buyer_name='Test Buyer Name',
                                        card_number='0123-4567-8901-2345',
                                        expiry='YYYY-mm',
                                        amount=1000,
                                        for_domestic=True,
                                        birth='YYmmDD',
                                        pwd_2digit='01')

        self.assertTrue(is_success)

        registration = Registration.objects.get(user=user,
                                                ticket=ticket)
        attend_check = AttendCheck.objects.get(registration=registration)
        payment_history = PaymentHistory.objects.get(registration=registration)

        self.assertEqual(registration.user.email, user.email)
        self.assertEqual(registration.ticket.id, ticket.id)
        self.assertFalse(registration.is_canceled)

        self.assertEqual(attend_check.registration.id, registration.id)
        self.assertFalse(attend_check.is_attended)

        self.assertEqual(payment_history.registration.id, registration.id)
        self.assertFalse(payment_history.is_canceled)
        self.assertIsNotNone(payment_history.imp_uid)
        self.assertIsNotNone(payment_history.merchant_uid)

        # TODO: After saving the above data
        # def test_cancel_registration_domestic(self):
        #     user = User.objects.get(email='test@email.com')
        #     registration = Registration.objects.get(user=user)
        #     payment_history = PaymentHistory.objects.get(registration=registration)
        #     is_success = Counter.cancel_registration(registration=registration,
        #                                              for_domestic=True)
        #
        #     self.assertTrue(is_success)
        #     self.assertTrue(payment_history.is_canceled)
        #     self.assertTrue(registration.is_canceled)
