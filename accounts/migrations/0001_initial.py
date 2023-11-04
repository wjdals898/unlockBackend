# Generated by Django 4.2.1 on 2023-06-16 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, null=True)),
                ("social_id", models.PositiveIntegerField(null=True, unique=True)),
                ("email", models.EmailField(max_length=40, unique=True)),
                ("gender", models.CharField(max_length=10, null=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Counselor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "userkey",
                    models.ForeignKey(
                        db_column="userkey",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="counselor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Counselee",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "userkey",
                    models.ForeignKey(
                        db_column="userkey",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="counselee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]