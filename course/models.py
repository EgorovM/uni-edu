import datetime

from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField

from student.models import Student
from school.models import School


class Course(models.Model):
    SPECIALIZATION = (
        ('CR', 'Творческий'),
        ('TH', 'Технический'),
        ('SP', 'Спортивный')
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    name = models.CharField(max_length=127)
    short_desc = models.CharField(max_length=255)

    description = RichTextField()
    specialization = models.CharField(max_length=3, choices=SPECIALIZATION)
    max_count = models.IntegerField(default=25)

    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.school} @{self.name}"

    def get_specialization(self):
        return dict(self.SPECIALIZATION)[self.specialization]


class Teacher(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    name = models.CharField(max_length=127)
    description = RichTextField()

    telephone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.course}-{self.name}"


class Feedback(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    author_name = models.CharField(max_length=127)

    content = RichTextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course}-{self.author_name}"
