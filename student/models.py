from django.contrib.auth import get_user_model
from django.db import models

from school.models import School


User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    telephone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)
    parent_telephone = models.CharField(max_length=11, null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    def from_request(request):
        student = Student()

        fields = ['telephone', 'email', 'parent_telephone', 'parent_email']

        for field in fields:
            if field in request.POST:
                setattr(student, field, request.POST[field])

        if 'image' in request.FILES:
            student.image = request.FILES['image']

        school = School.objects.get(id=request.POST['school'])
        student.school = school

        return student

    @property
    def name(self):
        return self.user.name
        
