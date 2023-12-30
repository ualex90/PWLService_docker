from django.urls import path
from rest_framework import routers

from app_pwl.apps import AppPwlConfig
from app_pwl.views.course import *
from app_pwl.views.lesson import *


app_name = AppPwlConfig.name

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name="lesson_list"),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path('lesson/create/', LessonCreateAPIView.as_view(), name="lesson_create"),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name="lesson_update"),
    path('lesson/<int:pk>/destroy/', LessonDestroyAPIView.as_view(), name="lesson_destroy"),
]

router = routers.SimpleRouter()
router.register('course', CourseViewSet)

urlpatterns += router.urls
