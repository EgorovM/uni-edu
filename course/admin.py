from django.contrib import admin

from .models import Course, Teacher, Feedback


admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Feedback)
