from rest_framework import serializers

from app_payment.models import StripeSession


class StripeSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeSession
        fields = '__all__'
        read_only_fields = ('user', 'create_date', 'payment_amount', 'session_url')

