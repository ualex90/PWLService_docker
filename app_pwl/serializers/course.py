from rest_framework import serializers
from rest_framework.fields import IntegerField, ListField

from app_pwl.models import Course
from app_pwl.serializers.lesson import LessonListSerializer
from app_subscriptions.serializers.course import SubscribeCourseSerializer


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner', 'stripe_product_id', 'stripe_prise_id')


class CourseListSerializer(serializers.ModelSerializer):
    lesson_count = IntegerField()  # Поле определяется в queryset во view
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribe(self, instance):
        return bool(instance.subscribers.filter(user=self.context.get("request").user))


class CourseRetrieveSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
