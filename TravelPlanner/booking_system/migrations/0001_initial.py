# Generated by Django 5.1.5 on 2025-04-08 11:17

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Agent",
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
                ("company", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region="NO"
                    ),
                ),
                ("website", models.URLField(blank=True)),
                ("note", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Basis",
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
                ("code", models.CharField(max_length=3)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Currency",
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
                ("name", models.CharField(max_length=32)),
                ("code", models.CharField(max_length=3)),
            ],
            options={
                "verbose_name_plural": "Currencies",
            },
        ),
        migrations.CreateModel(
            name="Generated",
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
                ("title", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentStatus",
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
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "PaymentStatuses",
            },
        ),
        migrations.CreateModel(
            name="ServiceType",
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
                ("title", models.CharField(max_length=255, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "ServiceTypes",
            },
        ),
        migrations.CreateModel(
            name="Supplier",
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
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="TripStatus",
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
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "TripStatuses",
            },
        ),
        migrations.CreateModel(
            name="Consultant",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("NOR", "Norwegian"),
                            ("ZAR", "South African"),
                            ("Other", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Guest",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("middle_name", models.CharField(blank=True, max_length=50, null=True)),
                ("date_of_birth", models.DateField()),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "mobile",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region="NO"
                    ),
                ),
                (
                    "emergency_contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="emergency_for",
                        to="booking_system.guest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trip",
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
                ("name", models.CharField(max_length=64)),
                ("number_of_guests", models.IntegerField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "guests",
                    models.ManyToManyField(
                        related_name="guests", to="booking_system.guest"
                    ),
                ),
                (
                    "no_consultant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="no_consultant_trips",
                        to="booking_system.consultant",
                    ),
                ),
                (
                    "payment_status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.paymentstatus",
                    ),
                ),
                (
                    "sa_consultant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sa_consultant_trips",
                        to="booking_system.consultant",
                    ),
                ),
                (
                    "trip_status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.tripstatus",
                    ),
                ),
            ],
            options={
                "ordering": ["start_date"],
            },
        ),
        migrations.CreateModel(
            name="Service",
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
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "reservation_number",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("tax_invoice", models.BooleanField(blank=True, null=True)),
                ("paid", models.BooleanField(blank=True, null=True)),
                ("paid_date", models.DateField(blank=True, null=True)),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.currency",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.servicetype",
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.supplier",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.trip",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Flight",
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
                ("number", models.CharField(max_length=16)),
                ("arrival_date", models.DateField(blank=True, null=True)),
                ("arrival_time", models.TimeField(blank=True, null=True)),
                (
                    "arrival_airport",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("departure_date", models.DateField(blank=True, null=True)),
                ("departure_time", models.TimeField(blank=True, null=True)),
                (
                    "departure_airport",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("booked_by", models.CharField(max_length=16)),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.currency",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="booking_system.trip",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Accommodation",
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
                ("units", models.IntegerField(blank=True, null=True)),
                ("arrival_date", models.DateField()),
                ("departure_date", models.DateField()),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "reservation_number",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("tax_invoice", models.BooleanField(blank=True, null=True)),
                ("paid", models.BooleanField(blank=True, null=True)),
                ("paid_date", models.DateField(blank=True, null=True)),
                ("note", models.TextField(blank=True)),
                (
                    "basis",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.basis",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.currency",
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.supplier",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="booking_system.trip",
                    ),
                ),
            ],
        ),
    ]
