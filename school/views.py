from django.shortcuts import render

from .models import School, Advert


def schools(request):
    type = request.GET.get('type', '')
    schools = School.objects.filter(type__startswith=type)

    full_type = dict(School.EDU_TYPES)[type]

    return render(request, 'school/schools.html', locals())


def school(request, id):
    school = School.objects.get(id=id)

    return render(request, 'school/school.html', locals())


def adverts(request):
    adverts = Advert.objects.all().order_by('pub_date')

    return render(request, 'advert/adverts.html', locals())


def advert(request, id):
    advert = Advert.objects.get(id=id)

    return render(request, 'advert/advert.html', locals())


def edit_advert(request, id):
    advert = Advert.objects.get(id=id)

    if request.user != advert.school:
        return render(request, 'bad_access.html')

    return render(request, 'advert/edit_advert.html', locals())
