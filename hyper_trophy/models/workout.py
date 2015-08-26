# -*- coding: utf-8 -*-
"""This module contains the database models which are used to store information
about the different aspects of a particular workout.
"""
from django.db import models

from picklefield.fields import PickledObjectField

__all__ = ['EXCERCISE_CATEGORIES', 'MUSCLE_GROUPS', 'EXERCISE_MECHANICS',
           'DIFFICULTY_LEVELS', 'FORCES', 'EXERCISE_TYPES', 'Exercise', 'Set',
           'Workout']

EXCERCISE_CATEGORIES = (('R', 'Resistance'),
                        ('F', 'Functional'),
                        ('C', 'Cardio'))

MUSCLE_GROUPS = (('Q', 'Quadriceps'),
                 ('LB', 'Lower Back'),
                 ('B', 'Biceps'),
                 ('C', 'Chest'),
                 ('A', 'Abdominals'),
                 ('H', 'Hamstrings'),
                 ('T', 'Triceps'),
                 ('TR', 'Traps'),
                 ('M', 'Middle Back'),
                 ('L', 'Lats'),
                 ('N', 'Neck'),
                 ('F', 'Forearms'),
                 ('G', 'Glutes'),
                 ('S', 'Shoulders'),
                 ('CA', 'Calves'))

EXERCISE_MECHANICS = (('C', 'Compound'),
                      ('I', 'Isolation'))

DIFFICULTY_LEVELS = (('B', 'Beginner'),
                     ('I', 'Intermediate'),
                     ('E', 'Expert'))

FORCES = (('PS', 'Push'),
          ('PL', 'Pull'),
          ('ST', 'Static'))

EXERCISE_TYPES = (('C', 'Cardio'),
                  ('O', 'Olympic Weightlifting'),
                  ('PL', 'Plyometrics'),
                  ('PW', 'Powerlifting'),
                  ('ST', 'Strength'),
                  ('SR', 'Stretching'),
                  ('SM', 'Strongman'))


def _l_to_s(value, options):
    """Convert a long option to a short option. Useful for converting between
    human readable and actual CHOICES for choice fields
    """
    for short, long in options:
        if value == long:
            return short
    return value


class Exercise(models.Model):
    """A Base model type for storing data about a particular exercies"""
    #: The name of this exercise
    name = models.CharField(max_length=120)

    #: The rate at which weight/reps for this excercise should be increased by
    progress_differential = models.FloatField(null=True, blank=True)

    #: Primary muscle group impacted by this exercise
    primary_muscle_group = models.CharField(max_length=2,
                                            choices=MUSCLE_GROUPS)

    #: Secondary muscle group impacted by this exercise
    secondary_muscle_group = models.CharField(max_length=2, null=True,
                                              blank=True,
                                              choices=MUSCLE_GROUPS)

    #: What "type" of exercise is this?
    category = models.CharField(max_length=1, choices=EXCERCISE_CATEGORIES)

    #: Aliases for this Exercise
    also_known_as = models.CharField(max_length=120)

    #: One of Compound or Isolation, describing the mechanics of this exercise
    mechanics_type = models.CharField(max_length=1, choices=EXERCISE_MECHANICS,
                                      null=True, blank=True)

    #: A link to a heatmap image of the muscles impacted by this exercise
    muscle_image = models.URLField()

    #: A newline separated textual guide to this exercise
    guide = models.TextField()

    #: One of Beginner, Intermediate, Expert. Indicating the level of skill
    #: required to perform this exercise successfully
    difficulty_level = models.CharField(max_length=1,
                                        choices=DIFFICULTY_LEVELS)

    #: Free form text describing any equipment required to perform this
    #: exercise
    equipment = models.TextField()

    #: The direction of force applied to perform this exercise. Will be one of
    #: Push, Pull, Static, or None
    force = models.CharField(max_length=2, choices=FORCES, null=True,
                             blank=True)

    #: This exercises type
    type = models.CharField(max_length=2, choices=EXERCISE_TYPES)

    @classmethod
    def from_json(cls, name, **kwargs):
        """Create a new Exercise based off of the provided key and JSON data

        :param name: The name of this exercise
        :param kwargs: The remaining data for this Exercise
        """
        arguments = {}
        for k, val in kwargs.items():
            key = k.replace(' ', '_').lower()

            if key in ['your_rating', 'stretch_type']:
                continue
            elif key in ['also_known_as', 'muscle_image', 'guide',
                         'equipment']:
                arguments[key] = kwargs.get(k).strip()
            elif key == 'mechanics_type':
                arguments[key] = _l_to_s(kwargs.get(k).strip(),
                                         EXERCISE_MECHANICS)
            elif key == 'force':
                arguments[key] = _l_to_s(kwargs.get(k).strip(), FORCES)
            elif key == 'type':
                arguments[key] = _l_to_s(kwargs.get(k).strip(), EXERCISE_TYPES)
            elif key == 'main_muscle_worked':
                group = kwargs.get(k).strip()
                arguments['primary_muscle_group'] = _l_to_s(group,
                                                            MUSCLE_GROUPS)
            elif key == 'other_muscles':
                group = kwargs.get(k).strip()
                arguments['secondary_muscle_group'] = _l_to_s(group,
                                                              MUSCLE_GROUPS)
            elif key == 'level':
                arguments['difficulty_level'] = _l_to_s(kwargs.get(k).strip(),
                                                        DIFFICULTY_LEVELS)
        Exercise(name=name, **arguments).save()

    def __str__(self):
        return '<Exercise: {}>'.format(self.name)
    __unicode__ = __repr__ = __str__


class Set:
    """A basic object (not model) that is used to encapsulate a single set of a
    particular exercise
    """

    def __init__(self, exercise, reps, weight=None):
        """Create a new :class:`Set` instance.

        :param exercise: The exercise to be performed during this set
        :param reps: How many reps
        :param weight: The weight at which to perform *reps* of *exercise*.
            Defaults to :const:`None` for body weight or cardio exercises
        """
        self.exercise = exercise
        self.reps = reps
        self.weight = weight

    def feedback(self, feedback):
        pass


class Workout(models.Model):
    """A Collection of sets compiled into an individual workout"""

    #: The collection of sets in this workout
    sets = PickledObjectField(compress=True)

    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)

    #: The target muscle group for this workout
    target = models.CharField(max_length=2, choices=MUSCLE_GROUPS)

    def duration(self):
        """Compare the end and start time for the duration of this workout"""
        return self.completed - self.started

    def __iter__(self):
        """Iterate over the sets in this workout"""
        return self.sets.__iter__()
