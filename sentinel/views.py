from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.conf import settings
from django.views import View

from .models import EmailToken, EmailUser
from .forms import EmailLoginForm

from .async_email_sender import send_mail


class LoginView(View):
    form_class = EmailLoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()

            self.send_email_token(request, token)
            return render(request, 'mailsent.html')

        return render(request, self.template_name, {'form': form})

    def send_email_token(self, request, token):
        html = render_to_string('mail/email_token.html', {'token': token}, request)

        send_mail(
            "파이콘 세미나 일회용 로그인 토큰",
            html,
            settings.EMAIL_HOST_USER,
            [token.email],
            html=html,
        )


class CheckTokenView(View):

    def get(self, request, token):
        time_threshold = datetime.now() - timedelta(hours=1)
        try:
            token = EmailToken.objects.get(token=token, created_at__gte=time_threshold)
        except ObjectDoesNotExist:
            return render(request, 'invalidtoken.html')

        email = token.email
        try:
            user = EmailUser.objects.get(email=email)
        except ObjectDoesNotExist:
            user = EmailUser.objects.create_user(email)
            # user.save()

        login(request, user)
        token.delete()

        return redirect(reverse('index'))


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
