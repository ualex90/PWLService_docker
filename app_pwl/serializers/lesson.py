from rest_framework import serializers

from app_pwl.validators import LinkValidator
from app_pwl.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ('owner', 'stripe_product_id', 'stripe_prise_id')
        validators = [
            LinkValidator('video', 'name', 'description', 'body')
        ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'name', 'description', )
