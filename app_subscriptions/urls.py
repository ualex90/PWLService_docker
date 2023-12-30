from django.urls import path

from app_subscriptions.apps import AppSubscriptionsConfig
from app_subscriptions.views.course import SubscribeCreateCourseAPIView, SubscribeDestroyCourseAPIView

app_name = AppSubscriptionsConfig.name

urlpatterns = [
    path('course/', SubscribeCreateCourseAPIView.as_view(), name="subscribe_course"),
    path('course/<int:pk>/destroy', SubscribeDestroyCourseAPIView.as_view(), name="unsubscribe_course"),
]
