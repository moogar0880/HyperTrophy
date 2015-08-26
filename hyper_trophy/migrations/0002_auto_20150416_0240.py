# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hyper_trophy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerprofile',
            name='is_configured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_configured',
            field=models.BooleanField(default=False),
        ),
    ]
