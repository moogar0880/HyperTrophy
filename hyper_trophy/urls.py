from django.conf.urls import patterns, url, include
from django.contrib import admin

from .views import (WorkoutView, HomeView, RegistrationView, LoginView,
                    LogoutView)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register/', RegistrationView.as_view(), name='register'),
    url(r'^fitness/', WorkoutView.as_view(), name='fitness'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^admin/', include(admin.site.urls)),

)
