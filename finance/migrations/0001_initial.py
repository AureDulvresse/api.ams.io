# Generated by Django 5.1.5 on 2025-01-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("number", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("type", models.CharField(max_length=50)),
                ("balance", models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name="SchoolFee",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("due_date", models.DateField()),
                (
                    "paid_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("status", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
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
                ("date", models.DateField()),
                ("description", models.TextField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("type", models.CharField(max_length=50)),
            ],
        ),
    ]
