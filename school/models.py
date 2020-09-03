import re

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
    image = models.ImageField(upload_to='school/')

    description = RichTextField()
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=11)
    child_amount = models.IntegerField(default=0)
    min_grade = models.IntegerField(default=5)
    max_grade = models.IntegerField(default=11)

    email = models.EmailField()

    site = models.CharField(max_length=63, blank=True)

    def __str__(self):
        return self.name

    def get_edu_type(self):
        return dict(self.EDU_TYPES)[self.type]

    @property
    def locality(self):
        return self.address.split(',')[1]

    @property
    def pretty_telephone(self):
        tel = self.telephone

        return f"+{tel[0]} ({tel[1:5]}) {tel[5:7]}-{tel[7:9]}-{tel[9:]}"

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
