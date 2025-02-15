# Generated by Django 5.1.5 on 2025-01-19 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("finance", "0001_initial"),
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="schoolfee",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="student.student"
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="finance.account"
            ),
        ),
    ]
