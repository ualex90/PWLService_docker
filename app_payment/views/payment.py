from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from app_payment.models import Payment
from app_payment.paginators import PaymentPaginator
from app_payment.serializers.payment import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    """ Get payment list"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('date',)
    filterset_fields = ('course', 'lesson', 'payment_method', )
    pagination_class = PaymentPaginator

