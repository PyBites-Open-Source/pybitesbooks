# Generated by Django 3.2.5 on 2021-08-23 08:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0031_alter_importedbook_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookconversion',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
