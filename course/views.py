from django.shortcuts import render

from course.models import Course, Feedback


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

    return render(request, 'course/course.html', locals())
