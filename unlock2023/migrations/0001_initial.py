# Generated by Django 4.2.1 on 2023-06-19 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0004_alter_user_last_login"),
    ]

    operations = [
        migrations.CreateModel(
            name="CounselingType",
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
                ("type", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
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
                    "time",
                    models.CharField(
                        choices=[
                            ("09:00", "1"),
                            ("10:00", "2"),
                            ("11:00", "3"),
                            ("12:00", "4"),
                            ("13:00", "5"),
                            ("14:00", "6"),
                            ("15:00", "7"),
                            ("16:00", "8"),
                            ("17:00", "9"),
                            ("18:00", "10"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "counselee_id",
                    models.ForeignKey(
                        db_column="counselee_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.counselee",
                    ),
                ),
                (
                    "counselor_id",
                    models.ForeignKey(
                        db_column="counselor_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.counselor",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        db_column="type",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="unlock2023.counselingtype",
                    ),
                ),
            ],
        ),
    ]
