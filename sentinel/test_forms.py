from django.test import TestCase

from .forms import EmailLoginForm


class EmailLoginFormTest(TestCase):

    def test_init(self):
        EmailLoginForm()

    def test_valid_data(self):
        form = EmailLoginForm({
            'email': "seminar@example.com"
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], "seminar@example.com")

    def test_blank_data(self):
        form = EmailLoginForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['필수 항목입니다.'],
        })
