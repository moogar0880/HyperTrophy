# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('progress_differential', models.FloatField(blank=True, null=True)),
                ('primary_muscle_group', models.CharField(choices=[('Q', 'Quadriceps'), ('LB', 'Lower Back'), ('B', 'Biceps'), ('C', 'Chest'), ('A', 'Abdominals'), ('H', 'Hamstrings'), ('T', 'Triceps'), ('TR', 'Traps'), ('M', 'Middle Back'), ('L', 'Lats'), ('N', 'Neck'), ('F', 'Forearms'), ('G', 'Glutes'), ('S', 'Shoulders'), ('CA', 'Calves')], max_length=2)),
                ('secondary_muscle_group', models.CharField(choices=[('Q', 'Quadriceps'), ('LB', 'Lower Back'), ('B', 'Biceps'), ('C', 'Chest'), ('A', 'Abdominals'), ('H', 'Hamstrings'), ('T', 'Triceps'), ('TR', 'Traps'), ('M', 'Middle Back'), ('L', 'Lats'), ('N', 'Neck'), ('F', 'Forearms'), ('G', 'Glutes'), ('S', 'Shoulders'), ('CA', 'Calves')], blank=True, null=True, max_length=2)),
                ('category', models.CharField(choices=[('R', 'Resistance'), ('F', 'Functional'), ('C', 'Cardio')], max_length=1)),
                ('also_known_as', models.CharField(max_length=120)),
                ('mechanics_type', models.CharField(choices=[('C', 'Compound'), ('I', 'Isolation')], blank=True, null=True, max_length=1)),
                ('muscle_image', models.URLField()),
                ('guide', models.TextField()),
                ('difficulty_level', models.CharField(choices=[('B', 'Beginner'), ('I', 'Intermediate'), ('E', 'Expert')], max_length=1)),
                ('equipment', models.TextField()),
                ('force', models.CharField(choices=[('PS', 'Push'), ('PL', 'Pull'), ('ST', 'Static')], blank=True, null=True, max_length=2)),
                ('type', models.CharField(choices=[('C', 'Cardio'), ('O', 'Olympic Weightlifting'), ('PL', 'Plyometrics'), ('PW', 'Powerlifting'), ('ST', 'Strength'), ('SR', 'Stretching'), ('SM', 'Strongman')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trainer_id', models.IntegerField()),
                ('completed', models.BooleanField(default=False)),
                ('workout_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('n_days_per_week', models.IntegerField(verbose_name='Days Per Week')),
                ('musclegroup_rotation', models.CharField(max_length=60)),
                ('included_exercises', models.ManyToManyField(to='hyper_trophy.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, null=True, max_length=120)),
                ('user_id', models.IntegerField()),
                ('template_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('ignored_exercises', models.ManyToManyField(to='hyper_trophy.Exercise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sets', picklefield.fields.PickledObjectField(editable=False)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('target', models.CharField(choices=[('Q', 'Quadriceps'), ('LB', 'Lower Back'), ('B', 'Biceps'), ('C', 'Chest'), ('A', 'Abdominals'), ('H', 'Hamstrings'), ('T', 'Triceps'), ('TR', 'Traps'), ('M', 'Middle Back'), ('L', 'Lats'), ('N', 'Neck'), ('F', 'Forearms'), ('G', 'Glutes'), ('S', 'Shoulders'), ('CA', 'Calves')], max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_workout',
            field=models.ForeignKey(null=True, blank=True, to='hyper_trophy.Workout'),
        ),
        migrations.AddField(
            model_name='trainerprofile',
            name='clients',
            field=models.ManyToManyField(to='hyper_trophy.UserProfile'),
        ),
    ]
