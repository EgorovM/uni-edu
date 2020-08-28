from django.db import models
from django.contrib.auth.models import User

from school.models import School

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    name = models.CharField(max_length=127)
    telephone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)
    parent_telephone = models.CharField(max_length=11, null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name
