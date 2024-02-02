from .forms import LoginForm, RegisterForm
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserRegistrationView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
