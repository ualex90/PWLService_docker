from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_subscriptions.models import Subscription
from app_subscriptions.serializers.course import SubscribeCourseSerializer
from app_users.permissions import IsModerator, IsSubscriber


class SubscribeCreateCourseAPIView(generics.CreateAPIView):
    """ Subscribe to the course """

    queryset = Subscription.objects.all()
    serializer_class = SubscribeCourseSerializer

    # Подписаться на курс может только пользователь. Модератору запрещено
    permission_classes = [IsAuthenticated, ~IsModerator]

    # пользователь создавший подписку, автоматически попадает в поле owner
    def perform_create(self, serializer):
        if not self.queryset.filter(user=self.request.user, course=self.request.data.get('course')).exists():
            new_subscribe = serializer.save()
            new_subscribe.user = self.request.user
            new_subscribe.save()


class SubscribeDestroyCourseAPIView(generics.DestroyAPIView):
    """ Unsubscribe to the course """

    queryset = Subscription.objects.all()
    serializer_class = SubscribeCourseSerializer

    # Удалить подписку может только тот кто ее создал
    permission_classes = [IsSubscriber]
