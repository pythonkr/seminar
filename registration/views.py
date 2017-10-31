from django.shortcuts import render
from django.views import View

from .forms import PaymentForm


class PaymentView(View):
    form_class = PaymentForm
    template_name = 'payment.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
