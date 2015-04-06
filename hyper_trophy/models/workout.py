# -*- coding: utf-8 -*-
"""This module contains the database models which are used to store information
about the different aspects of a particular workout.
"""
from django.db import models

from picklefield.fields import PickledObjectField

__all__ = ['EXCERCISE_CATEGORIES', 'MUSCLE_GROUPS', 'Exercise', 'Set',
           'Workout']

EXCERCISE_CATEGORIES = (('R', 'Resistance'),
                        ('F', 'Functional'),
                        ('C', 'Cardio'))

MUSCLE_GROUPS = (('CH', 'Chest'),
                 ('L', 'Legs'),
                 ('T', 'Triceps'),
                 ('BA', 'Back'),
                 ('BI', 'Biceps'),
                 ('CO', 'Core'),
                 ('S', 'Shoulders'))


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

    #: The size of the area of the primary muscle group impacted by this
    #: exercise. Used for sorting the exercises in a workout in order to ensure
    #: that larger muscles are worked out prior to smaller muscle groups
    muscle_size = models.IntegerField()

    def __str__(self):
        return '<Exercise: {}>'.format(self.name)
    __unicode__ = __repr__ = __str__


class Set:
    """A basic object (not model) that is used to encapsulate a single set of a
    particular exercise
    """

    def __init__(self, exercise, reps):
        """Create a new :class:`Set` instance.

        :param exercise: The exercise to be performed during this set
        :param reps: How many reps
        """
        self.exercise = exercise
        self.reps = reps

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
