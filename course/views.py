import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from course.models import Course, Teacher, Feedback, CourseAttendance
from student.models import Student
from school.models import School


def courses(request):
    type = request.GET.get('type', '')

    courses = Course.objects.filter(school__type__startswith=type)

    return render(request, 'course/courses.html', locals())


def course(request, id):
    course = Course.objects.get(id=id)

    if request.method == "POST":
        if 'send_feedback' in request.POST:
            fields = ['author_name', 'content']
            feedback = Feedback()

            for field in fields:
                setattr(feedback, field, request.POST.get(field))

            feedback.course = course
            feedback.save()

        elif 'apply' in request.POST:
            student = Student.objects.get(user=request.user)
            course.requests.add(student)
            course.save()

    return render(request, 'course/course.html', locals())


@login_required
def courses_requests(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == "POST":
        course_id = request.POST['course_id']
        course = Course.objects.get(id=course_id)

        student_id = request.POST['student_id']
        student = Student.objects.get(id=student_id)

        if 'access' in request.POST:
            course.students.add(student)
            student.user.send_access_notification(course)
        elif 'reject' in request.POST:
            student.user.send_reject_notification(course)

        course.requests.remove(student)

    return render(request, 'teacher/courses_requests.html', locals())


@login_required
def my_courses(request):
    models = [Teacher, School, Student]

    for may_model in models:
        model = may_model.objects.filter(user=request.user).first()

        if not model is None:
            break

    courses = model.course_set.all()
    today = datetime.datetime.now().date

    return render(request, 'course/my_courses.html', locals())


def attendance_mark(request):
    student_id = request.GET.get('student_id')
    course_id = request.GET.get('course_id')

    if not (student_id is None or course_id is None):
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        course_attendane = CourseAttendance.objects.get(
            course=course, date=datetime.datetime.now()
        )

        if student in course_attendane.students.all():
            course_attendane.students.remove(student)
        else:
            course_attendane.students.add(student)

        course_attendane.save()

    return HttpResponse('success')
