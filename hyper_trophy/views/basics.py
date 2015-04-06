# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm

from .base import HyperView
from ..models import UserProfile

__all__ = ['HomeView', 'RegistrationView']


class HomeView(HyperView):
    """Just a simple home page. Nothing to see here"""

    title = 'Home'
    template = 'home.html'


class RegistrationView(HyperView):
    title = 'Register'
    template = 'register.html'
    form_class = UserCreationForm


class LoginView(HyperView):
    pass


class LogoutView(HyperView):
    pass
