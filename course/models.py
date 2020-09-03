import datetime

from django.db import models
from django.contrib.auth import get_user_model
from djrichtextfield.models import RichTextField

from student.models import Student
from school.models import School


User = get_user_model()


class Course(models.Model):
    SPECIALIZATION = (
        ('CR', 'Творческий'),
        ('TH', 'Технический'),
        ('SP', 'Спортивный')
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    students = models.ManyToManyField(Student, blank=True)
    requests = models.ManyToManyField(Student, blank=True, related_name='requests')

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

    @property
    def attendance(self):
        return CourseAttendance.objects.get(
            course=self, date=datetime.datetime.now()
        ).students.all()

    def from_request(request):
        course = Course()
        course.fill_by_request(request)

        return course

    def fill_by_request(self, request):
        fields = ['name', 'short_desc', 'description',
                  'max_count', 'specialization']

        for field in fields:
            if field in request.POST:
                setattr(self, field, request.POST[field])

        teacher_id = request.POST['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)

        self.teacher = teacher


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='teachers/', default='teachers/default.jpg')
    description = RichTextField()

    birthday = models.DateField(default=datetime.datetime(2001, 1, 1))
    city = models.CharField(max_length=63, default='Нюрба')
    languages_list = models.CharField(max_length=100, default='Якутский язык; Русский язык;')

    experience = models.IntegerField(default=0)
    education = models.CharField(max_length=255)

    telephone = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.school}-{self.name}"

    def from_request(request, school):
        teacher = Teacher()
        teacher.fill_by_request(request)

        number_in_school = Teacher.objects.filter(school=school).count() + 1
        username = f'{school.user.username}_{number_in_school}'

        user = User.objects.create_user(
            username=username,
            name=request.POST['name'],
            password='password_' + username,
            type='TH',
        )

        teacher.user = user

        return teacher

    def fill_by_request(self, request):
        fields = ['description', 'city', 'languages_list',
                  'experience', 'education', 'telephone', 'email']

        for field in fields:
            if field in request.POST:
                setattr(self, field, request.POST[field])

        birthday = datetime.datetime.strptime(
            request.POST['birthday'], '%Y-%m-%d')

        if not self.user is None:
            self.user.name = request.POST['name']
            
        setattr(self, 'birthday', birthday)

        if 'image' in request.FILES:
            setattr(self, 'image', request.FILES['image'])

    @property
    def name(self):
        return self.user.name

    @property
    def pretty_telephone(self):
        tel = self.telephone
        return f"+{tel[0]} ({tel[1:4]}) {tel[4:7]} {tel[7:]}"

    @property
    def languages(self):
        return " ".join(self.languages_list.split(';'))


class Feedback(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    author_name = models.CharField(max_length=127)

    content = RichTextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course}-{self.author_name}"


class CourseAttendance(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.course) + ' посещаемость на ' + str(self.date)
