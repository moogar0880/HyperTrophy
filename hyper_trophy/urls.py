# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin

from .views import (WorkoutView, HomeView, RegistrationView, LoginView,
                    LogoutView, WorkoutBackgroundView)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register/', RegistrationView.as_view(), name='register'),
    url(r'^workout/', WorkoutView.as_view(), name='workout'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^background/basic/', WorkoutBackgroundView.as_view(),
        name='basic_background'),
    url(r'^background/advanced/', WorkoutBackgroundView.as_view(),
        name='advanced_background'),
    url(r'^background/', WorkoutBackgroundView.as_view(), name='background'),
    url(r'^admin/', include(admin.site.urls)),

)
