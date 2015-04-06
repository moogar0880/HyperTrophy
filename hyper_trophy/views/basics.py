# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

from .base import HyperView
from ..models import UserProfile

__all__ = ['HomeView', 'RegistrationView', 'LoginView', 'LogoutView']


class HomeView(HyperView):
    """Just a simple home page. Nothing to see here"""

    title = 'Home'
    template = 'home.html'


class RegistrationView(HyperView):
    """View for handling basic user registration"""

    title = 'Register'
    template = 'register.html'
    form_class = UserCreationForm

    def post(self, request):
        """If we successfully created a user, attach a User Profile to it"""
        sup = super(RegistrationView, self).post(request)
        if self.form.is_valid():
            user = self.form.save()
            UserProfile(user_id=user.id).save()
        return sup


class LoginView(HyperView):
    """View for handling user session information"""

    title = 'Login'
    template = 'login.html'
    form_class = AuthenticationForm

    def post(self, request):
        """Try logging in, return message on success, error on failure"""
        self.form = self.form_class(request, request.POST)
        user = authenticate(username=self.form['username'].value(),
                            password=self.form['password'].value())
        if user is None:
            login_err = 'Incorrect username or password. Please try again.'
            self.form.add_error(None, login_err)
        else:
            login(self.request, user)
            messages.success(self.request, 'Login Successfull')

        return super(LoginView, self).post(request)


class LogoutView(HyperView):
    """View for handling logging out"""

    def get(self, request):
        """Log out and redirect"""
        logout(request)

        # Do some path hacking to make the messages stick
        request.path = request.META['HTTP_REFERER']
        messages.success(request, 'Logged out successfully.')
        return redirect(request.path)
