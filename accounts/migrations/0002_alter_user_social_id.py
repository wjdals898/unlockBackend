# Generated by Django 4.2.1 on 2023-06-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="social_id",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
