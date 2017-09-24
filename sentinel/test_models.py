from django.test import TestCase

from .models import EmailToken, EmailUser


class EmailTokenModelTest(TestCase):
    def test_generate_email_token(self):
        email_token = EmailToken(email='seminar@example.com')
        self.assertEqual(len(email_token.token.__str__), 16)


class EmailUserModelTest(TestCase):        
    def test_string_representation(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(str(user), user.email)
    
    def test_get_users_full_name(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(user.get_full_name(), user.email)

    def test_get_users_short_name(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(user.get_short_name(), user.email)

    def test_user_has_perm(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertTrue(user.has_perm(None))

    def test_user_has_modules_perm(self):
        user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertTrue(user.has_module_perms(None))

    def test_user_is_staff(self):
        common_user = EmailUser.objects.create_user(email='seminar@example.com')
        self.assertEqual(common_user.is_staff, False)
        admin_user = EmailUser.objects.create_superuser(email='admin@example.com', password='password')
        self.assertEqual(admin_user.is_staff, True)
