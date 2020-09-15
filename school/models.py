import re
import datetime

from django.db import models
from django.contrib.auth import get_user_model

from djrichtextfield.models import RichTextField


User = get_user_model()


class School(models.Model):
    EDU_TYPES = (
        ('CE', 'Детское образовательное учреждение'),
        ('SE', 'Образовательное учреждение'),
        ('AE', 'Дополнительное образование')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=2, choices=EDU_TYPES)
    image = models.ImageField(upload_to='schools/', default="schools/default.png")

    description = RichTextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=11, blank=True)
    child_amount = models.IntegerField(default=0)
    min_grade = models.IntegerField(default=5)
    max_grade = models.IntegerField(default=11)

    headteacher = models.CharField(max_length=127, blank=True)
    subheadteacher = models.CharField(max_length=127, blank=True)

    foundation_date = models.DateField(null=True, blank=True)

    email = models.EmailField(blank=True)
    site = models.CharField(max_length=63, blank=True)

    def __str__(self):
        return self.name

    def get_edu_type(self):
        return dict(self.EDU_TYPES)[self.type]

    def fill_by_request(self, request):
        self.user.name = request.POST['name']
        self.user.save()

        fields = ['description', 'address', 'telephone', 'child_amount',
            'min_grade', 'max_grade', 'headteacher', 'subheadteacher',
            'email', 'site']

        for field in fields:
            if field in request.POST:
                setattr(self, field, request.POST.get(field, ''))

        if 'image' in request.FILES:
            self.image = request.FILES['image']

        self.foundation_date = datetime.datetime.strptime(
            request.POST['foundation_date'], '%Y-%m-%d')

        self.save()

    @property
    def locality(self):
        if len(self.address.split(',')) >= 2:
            return self.address.split(',')[1]

        return ""

    @property
    def pretty_telephone(self):
        tel = self.telephone

        if len(tel) == 11:
            return f"+{tel[0]} ({tel[1:5]}) {tel[5:7]}-{tel[7:9]}-{tel[9:]}"

        return ""

    @property
    def name(self):
        return self.user.name


class Advert(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='adverts/', default='adverts/default.jpg')
    title = models.CharField(max_length=127)
    content = RichTextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def from_request(request):
        advert = Advert()
        advert.fill_by_request(request)

        return advert

    def fill_by_request(self, request):
        fields = ['title', 'content']

        for field in fields:
            if field in request.POST:
                setattr(self, field, request.POST[field])

        if 'image' in request.FILES:
            self.image = request.FILES['image']

    @property
    def short_desc(self):
        return re.search(r'(<p.+?</p>)', self.content).group(0)
