from django.conf.urls import url

from .views import PaymentView

urlpatterns = [
    url(r'^$', PaymentView.as_view(), name='payment_index'),
]
