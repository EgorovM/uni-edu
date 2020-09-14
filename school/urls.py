from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('schools/', views.schools, name='schools'),
    path('school/<int:id>', views.school, name='school'),

    path('adverts/', views.adverts, name='adverts'),
    path('advert/<int:id>', views.advert, name='advert'),
    path('add_advert/', views.add_advert, name='add_advert'),
    path('edit_advert/<int:id>', views.edit_advert, name='edit_advert'),

    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<int:id>', views.edit_course, name='edit_course'),

    path('teachers/<int:school_id>', views.teachers, name='teachers'),
    path('teacher/<int:id>', views.teacher, name='teacher'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('edit_teacher/<int:id>', views.edit_teacher, name='edit_teacher'),
]
