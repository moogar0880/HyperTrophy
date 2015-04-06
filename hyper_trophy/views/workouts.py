# -*- coding: utf-8 -*-
from .base import HyperView
from ..forms import WorkoutForm

__all__ = ['WorkoutView']


class WorkoutView(HyperView):
    title = 'Workout'
    template = 'workout.html'
    form_class = WorkoutForm

    def get_post_data(self):
        exercises = select_exercises(self.request.POST.get('muscle_group'))
        sets = generate_sets(exercises)

        return {'sets': sets, 'form': WorkoutForm}
