from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views


urlpatterns = [
    path('schools/', views.schools, name='schools'),
    path('school/<int:id>', views.school, name='school'),

    path('adverts/', views.adverts, name='adverts'),
    path('advert/<int:id>', views.advert, name='advert'),
]
