# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import View

__all__ = ['HyperView']


class HyperView(View):
    """Base view type for all HyperTrophy views"""
    title = template = form_class = None

    def __init__(self, **kwargs):
        """Generate clean, per-instance attributes"""
        super(HyperView, self).__init__(**kwargs)
        self.context = {}
        self.request = self.form = None

    def get(self, request):
        """Generic get method"""
        if self.form_class is not None:
            self.form = self.form_class(request.POST, request.FILES)
        return render(request, self.template, self.get_context(),
                      context_instance=RequestContext(self.request))

    def post(self, request):
        """Generic post method"""
        self.request = request
        if self.form_class is not None and self.form is None:
            self.form = self.form_class(request.POST, request.FILES)
        return render(self.request, self.template,
                      self.get_context(
                          **self.get_post_data()
                      ),
                      context_instance=RequestContext(self.request))

    def get_context(self, **kwargs):
        """Return the context for the current view"""
        context = dict(
            form=self.form,
            title=self.title
        )
        context.update(self.context)
        context.update(kwargs)
        return context

    def get_post_data(self):
        """Return any additional context data for the result of a views post"""
        return dict()
