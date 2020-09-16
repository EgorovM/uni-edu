from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from school.models import School, Advert
from course.models import Course, Teacher, CourseAttendance



def index(request):
    return redirect('/courses')


@login_required()
def schools(request):
    type = request.GET.get('type', '')
    schools = School.objects.filter(type__startswith=type)

    TYPES = School.EDU_TYPES
    full_type = dict(School.EDU_TYPES)[type]

    return render(request, 'school/schools.html', locals())


@login_required()
def school(request, id):
    school = School.objects.get(id=id)

    return render(request, 'school/profile.html', locals())


@login_required()
def edit_info(request):
    school = School.objects.get(user=request.user)

    if request.method == "POST":
        if "save" in request.POST:
            school.fill_by_request(request)

    return render(request, 'school/edit-info.html', locals())


@login_required()
def adverts(request):
    school_name = request.GET.get('school_name', '')
    adverts = Advert.objects.filter(school__user__name__startswith=school_name).order_by('pub_date')

    return render(request, 'advert/adverts.html', locals())


@login_required()
def advert(request, id):
    advert = Advert.objects.get(id=id)
    return render(request, 'advert/advert.html', locals())


@login_required()
def add_advert(request):
    school = School.objects.get(user=request.user)

    if request.method == "POST":
        if "save" in request.POST:
            advert = Advert.from_request(request)
            advert.school = school
            advert.save()

            return redirect(reverse_lazy('advert', kwargs={"id": advert.id}))

    return render(request, 'advert/edit_advert.html', locals())


@login_required()
def edit_advert(request, id):
    school = School.objects.get(user=request.user)
    advert = Advert.objects.get(id=id)

    if school != advert.school:
        return render(request, 'bad_access.html')

    if request.method == "POST":
        if "save" in request.POST:
            advert.fill_by_request(request)
            advert.save()

            return redirect(reverse_lazy('advert', kwargs={"id": advert.id}))

        elif "delete" in request.POST:
            advert.delete()

            return redirect(reverse_lazy(
                    'adverts') + f'?school_name={school.name}')

    return render(request, 'advert/edit_advert.html', locals())


@login_required()
def add_course(request):
    school = School.objects.get(user=request.user)
    teachers = Teacher.objects.filter(school=school)
    SPECIALIZATION = Course.SPECIALIZATION

    if request.method == "POST":
        if "save" in request.POST:
            course = Course.from_request(request)
            course.school = school
            course.save()

            CourseAttendance.objects.create(course=course)

            return redirect(reverse_lazy('course', kwargs={"id": course.id}))

    return render(request, 'course/edit_course.html', locals())


@login_required()
def edit_course(request, id):
    school = School.objects.get(user=request.user)
    course = Course.objects.get(id=id)

    if course.school != school:
        return redirect('/bad_access')

    teachers = Teacher.objects.filter(school=school)
    SPECIALIZATION = Course.SPECIALIZATION

    if request.method == "POST":
        if "save" in request.POST:
            course.fill_by_request(request)
            course.save()

            return redirect(reverse_lazy('course', kwargs={"id": course.id}))

        elif "delete" in request.POST:
            course.delete()

            return redirect(reverse_lazy('my_courses'))

    return render(request, 'course/edit_course.html', locals())


@login_required()
def teachers(request, school_id):
    teachers = Teacher.objects.filter(school__id=school_id)
    return render(request, 'teacher/teachers.html', locals())


@login_required()
def teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    title = teacher.name

    return render(request, 'teacher/profile.html', locals())


@login_required()
def add_teacher(request):
    school = School.objects.get(user=request.user)

    if request.method == "POST":
        if 'save' in request.POST:
            teacher = Teacher.from_request(request, school)
            teacher.school = school

            teacher.save()

            return redirect(reverse_lazy('teacher', kwargs={"id": teacher.id}))

    return render(request, 'teacher/edit_teacher.html', locals())


@login_required()
def edit_teacher(request, id):
    school = School.objects.get(user=request.user)
    teacher = Teacher.objects.get(id=id)

    if teacher.school != school:
        return redirect('/bad_access')

    if request.method == "POST":
        if 'save' in request.POST:
            teacher.fill_by_request(request)
            teacher.save()

        elif 'delete' in request.POST:
            teacher.user.delete()

            return redirect(reverse_lazy('teachers', kwargs={"school_id": school.id}))

    return render(request, 'teacher/edit_teacher.html', locals())
