# -*- coding: utf-8 -*-
from django import forms

from .models import MUSCLE_GROUPS, DIFFICULTY_LEVELS, Exercise

__author__ = 'Jon Nappi'


class WorkoutForm(forms.Form):
    muscle_group = forms.ChoiceField(choices=MUSCLE_GROUPS)


LAST_WORKOUT_CHOICES = (
    ('0', 'Today'),
    ('1', 'Yesterday'),
    ('2', 'Last Week'),
    ('3', 'Last Month'),
    ('4', '1-3 Months Ago'),
    ('5', '3-12 Months Ago'),
    ('6', 'Never')
)

SETUP_TYPE_CHOICES = (
    ('B', 'Basic'),
    ('A', 'Advanced')
)


class ExperienceForm(forms.Form):
    experience_level = forms.ChoiceField(choices=DIFFICULTY_LEVELS)

    last_workout = forms.ChoiceField(choices=LAST_WORKOUT_CHOICES)

    setup_type = forms.ChoiceField(choices=SETUP_TYPE_CHOICES)

    advanced_exercises = forms.MultipleChoiceField(
        choices=[(ex, ex) for ex in Exercise.objects.all()]
    )
