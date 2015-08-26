# -*- coding: utf-8 -*-
from functools import wraps
from django.shortcuts import redirect

from ..models import UserProfile


def user_notconfigured(func, to='/dashboard/'):
    """A decoartor (which assumes established authentication) that will
    redirect the user to their dashboard if their user profile has already
    been configured and they attempt to access an "account setup" type view
    """
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user_id=user.id)
        if profile.is_configured:
            return redirect(to=to)
        return func(self, request, *args, **kwargs)
    return inner
