# -*- coding: utf-8 -*-
"""This module contains the database models which are used to store information
about the different levels of users provided by this service, your basic user
and trainers.
"""
from django.contrib.auth.models import User
from django.db import models

__all__ = ['UserProfile', 'TrainerProfile']


class BaseProfile(models.Model):
    """Base profile class of functionality shared between all profile types"""

    #: The id of the user that this Profile maps to
    user_id = models.IntegerField(null=True, blank=True)

    @property
    def user(self):
        """Return the actual user object associated with this user's profile"""
        return User.objects.get(id=self.user_id)

    def get_dashboard(self):
        pass

    class Meta:
        abstract = True  # Don't actually create a db table for this model


class UserProfile(BaseProfile):
    """Profile of data and functionality to augment the builtin django user
    model
    """

    #: Exercises that the user doesn't want to be given
    ignored_exercises = models.ManyToManyField('Exercise',)

    @property
    def calendar(self):
        return None


class TrainerProfile(BaseProfile):
    """Profile of data relating to Trainer users"""

    #: The list of clients that this Trainer oversees
    clients = models.ManyToManyField('UserProfile')

    def get_dashboard(self):
        pass
