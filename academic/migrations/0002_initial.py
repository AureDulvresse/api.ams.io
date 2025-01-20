# Generated by Django 5.1.5 on 2025-01-19 09:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("academic", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="classgroup",
            name="head_teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="class_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="academic.classgroup"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="teachers",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="coursematerial",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="academic.course"
            ),
        ),
    ]
