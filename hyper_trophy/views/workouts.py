# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext

from .base import HyperView
from ..models import Trainer

__all__ = ['WorkoutView']


class WorkoutView(HyperView):
    title = 'Workout'
    template = 'workout.html'

    def get(self, request):
        trainer = Trainer.objects.get(user_id=request.user.id)
        return render(request, self.template,
                      self.get_context(workout=trainer.generate_workout()),
                      context_instance=RequestContext(self.request))
