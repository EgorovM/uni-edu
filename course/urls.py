from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views


urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('course/<int:id>', views.course, name='course')
]
