# Generated by Django 3.2.5 on 2021-08-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_auto_20210703_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookIdConversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodreads_id', models.CharField(max_length=20)),
                ('googlebooks_id', models.CharField(max_length=20)),
            ],
        ),
    ]
