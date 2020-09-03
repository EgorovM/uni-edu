from django.contrib import admin

from .models import Course, Teacher, Feedback, CourseAttendance


admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Feedback)
admin.site.register(CourseAttendance)
