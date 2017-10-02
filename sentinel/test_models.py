from django.test import TestCase

from .models import EmailToken, EmailUser


class EmailTokenModelTest(TestCase):
    def test_generate_email_token(self):
        email_token = EmailToken(email='seminar@example.com')
        self.assertEqual(len(email_token.email), 19)
        self.assertEqual(len(email_token.token.__str__()), 36)


class EmailUserModelTest(TestCase):        
    def test_string_representation(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(str(user), user.email)

    def test_user_is_staff(self):
        common_user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(common_user.is_staff, False)
        admin_user = EmailUser.objects.create_superuser(email='admin@example.com', password='password')
        self.assertEqual(admin_user.is_staff, True)
