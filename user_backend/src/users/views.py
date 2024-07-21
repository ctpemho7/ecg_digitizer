from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserLoginForm, UserRegisterForm
from users.models import UserModel
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Вход'


class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    title = 'Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!'
