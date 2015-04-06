from django.contrib import admin

from .models import (Exercise, Workout, Trainer, Template, UserProfile,
                     TrainerProfile)

for mdl in [Exercise, Workout, Trainer, Template, UserProfile, TrainerProfile]:
    admin.site.register(mdl)
