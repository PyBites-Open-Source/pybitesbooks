# Generated by Django 4.1.3 on 2023-06-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pomodoro", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pomodoro",
            name="end",
            field=models.DateTimeField(),
        ),
    ]
