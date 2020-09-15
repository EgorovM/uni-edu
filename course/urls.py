from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views


urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('course/<int:id>', views.course, name='course'),

    path('courses_requests', views.courses_requests, name='courses_requests'),
    path('my_courses', views.my_courses, name='my_courses'),

    path('update_attendance_days/', views.update_attendance_days),

    path('attendance_mark', views.attendance_mark, name='mark_attendance')
]
