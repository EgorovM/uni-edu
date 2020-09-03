from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('register/', views.register, name='register'),
]
