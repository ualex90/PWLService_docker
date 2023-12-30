from django.urls import path

from app_payment.apps import AppPaymentConfig
from app_payment.views.payment import PaymentListAPIView
from app_payment.views.stripe_session import PaymentCreateAPIView

app_name = AppPaymentConfig.name

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment_list'),
    path('new/', PaymentCreateAPIView.as_view(), name='new_payment'),
]
