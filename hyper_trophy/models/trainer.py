# -*- coding: utf-8 -*-
"""This module contains the database models which are used to store information
needed for planning and scheduling workouts
"""
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

import names

from .users import UserProfile
from .workout import Workout

__all__ = ['Trainer', 'ScheduleEntry', 'Template']


class Trainer(models.Model):
    """The :class:`Trainer` class encapsulates a per-user machine learning
    engine and workout scheduler which is responsible for intuitively
    generating workouts, based off of previous workouts, and updating planned
    workouts based on user feedback about previous workouts
    """

    #: The Personal trainer's name. Is allowed to be null, but will always
    #: be set.
    name = models.CharField(max_length=120, null=True, blank=True)

    #: The id of the user that this :class:`Trainer` is training
    user_id = models.IntegerField()

    #: The workout template to use to generate workouts from
    template_id = models.IntegerField()

    @property
    def template(self):
        return Template.objects.get(id=self.template_id)

    @property
    def user(self):
        """Return the actual user object associated with this Trainer"""
        return User.objects.get(id=self.user_id)

    @property
    def user_profile(self):
        return UserProfile.objects.get(user_id=self.user_id)

    @property
    def workout_schedule(self):
        """Return the workout schedule that this Trainer manages"""
        return ScheduleEntry.objects.filter(trainer_id=self.id)

    def _get_muscle_groups(self, template_str):
        return [ex.replace('[', '').replace(']', '').split(':')
                for ex in template_str.split(',')]

    def generate_workout(self):
        user_profile, template = self.user_profile, self.template
        muscle_lists = self._get_muscle_groups(template.musclegroup_rotation)

        if user_profile.last_workout is None:
            muscle_groups = muscle_lists[0]
        else:
            # Just in case, default to the first muscle grouping
            muscle_groups = muscle_lists[0]
            for mg in muscle_lists:
                if mg == user_profile.last_workout:
                    muscle_groups = mg

        exercises = [ex for ex in template.included_exercises
                     if ex not in user_profile.ignored_exercises and
                     ex.primary_muscle_group in muscle_groups]
        in_order = sorted(exercises, key=lambda x: x.muscle_size)
        return in_order

    def feedback(self):
        pass

    def schedule(self):
        pass

    def records(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Custom save method will dynamically generate a name of the Trainer
        doesn't already have one. This should only be the case when a
        :class:`Trainer` is first created
        """
        if self.name is None:
            self.name = names.get_first_name()
        if self.template_id is None:
            self.template_id = Template.get_default().id
        super(Trainer, self).save(force_insert, force_update, using,
                                  update_fields)


class ScheduleEntry(models.Model):

    #: A reference to the :class:`Trainer` responsible for managing this
    #: workout Schedule
    trainer_id = models.IntegerField()

    #: Has this scheduled workout been completed?
    completed = models.BooleanField(default=False)

    #: The id of the scheduled workout
    workout_id = models.IntegerField()

    @property
    def trainer(self):
        return Trainer.objects.get(id=self.trainer_id)

    @property
    def workout(self):
        return Workout.objects.get(id=self.workout_id)


class Template(models.Model):
    """Workout template for :class:`Trainer`s to use for generating workouts

    The musclegroup CharField must conform to the following CSV of lists
    notation. [group1],[group2:group3],[group4]...etc
    """

    #: The name of this template
    name = models.CharField(max_length=120)

    #: A description of the workout plan that this template describes
    description = models.TextField(null=True, blank=True)

    #: Exercises that are valid to be generated from the use of this template
    included_exercises = models.ManyToManyField('Exercise')

    #: days per week? other scheduling information?
    n_days_per_week = models.IntegerField(verbose_name='Days Per Week')

    #: muscle group rotation schema
    musclegroup_rotation = models.CharField(max_length=60)

    @classmethod
    def get_default(cls):
        """Return the default workout :class:`Template`"""
        try:
            return cls.objects.get(name='default')
        except ObjectDoesNotExist:
            # Create new default template if one doesn't already exist. Should
            # only ever be run once
            default = Template(
                name='default',
                n_days_per_week=5,
                musclegroup_rotation='[CH:T],[L],[BA:BI],[CO:S]'
            )
            default.save()

            from .workout import Exercise
            for ex in Exercise.objects.all():
                default.included_exercises.add(ex)
            default.save()
            return default

    def __str__(self):
        return '<Workout Template: {}>'.format(self.name)
    __unicode__ = __repr__ = __str__
