from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render
from django.db.models import Q

from school.models import School
from course.models import Teacher
from student.models import Student


User = get_user_model()

#TODO all

def login_view(request):
    title = "Вход"

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if not user is None:
            login(request, user)

            return redirect('/courses')
        else:
            error_text = "Неправильный логин или пароль"

    return render(request, 'registration/login.html', locals())


def register(request):
    title = "Регистрация"

    schools = School.objects.filter(~Q(type='AE'))
    accounts_types = User.ACCOUNTS_TYPES

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if authenticate(username=username, password=password) is None:
            user = User.objects.create_user(
                username=username,
                name=request.POST['name'],
                password=password,
                type='PR'
            )

            student = Student.from_request(request)
            student.user = user
            user.save()
            student.save()

            login(request, user)

            return redirect('/courses')
        else:
            error_text = 'Пользователь с таким именем уже существует'

    return render(request, 'registration/register.html', locals())
