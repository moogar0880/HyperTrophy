# -*- coding: utf-8 -*-
from .workout import Exercise


BUILTIN_EXERCISES = [
    {
        'name': 'Bench Press',
        'progress_differential': 0.35,
        'primary_muscle_group': 'CH',
        'category': 'R',
        'muscle_size': 9
    },
]


BUILTIN_TEMPLATES = [

]


def populate_exercises():
    for exercise in BUILTIN_EXERCISES:
        Exercise(**exercise).save()


def populate_templates():
    pass
