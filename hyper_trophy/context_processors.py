# -*- coding: utf-8 -*-
"""Additional context processors for the UI"""
from django.conf import settings
import hyper_trophy

__author__ = 'Jon Nappi'


def global_settings(request):
    """A global context processor for passing data that all templates will or
    may need access to
    """
    globals_dict = {
        'version': hyper_trophy.__version__,
    }

    return globals_dict
