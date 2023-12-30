from rest_framework import serializers

from app_subscriptions.models import Subscription


class SubscribeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('user', )
