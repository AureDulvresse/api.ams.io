# Generated by Django 5.1.5 on 2025-01-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("employee_id", models.CharField(max_length=20, unique=True)),
                ("contract_type", models.CharField(max_length=50)),
                ("hire_date", models.DateField()),
                ("department", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Leave",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("leave_type", models.CharField(max_length=50)),
                ("status", models.CharField(max_length=20)),
                ("reason", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("base_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "bonus",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "deductions",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("payment_date", models.DateField()),
                ("is_paid", models.BooleanField(default=False)),
            ],
        ),
    ]
