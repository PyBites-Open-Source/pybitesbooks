# Generated by Django 3.1.2 on 2020-10-27 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0020_userbook_favorite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userbook',
            options={'ordering': ['-favorite', '-completed', '-id']},
        ),
        migrations.AddField(
            model_name='book',
            name='similar_bookids',
            field=models.TextField(blank=True, null=True),
        ),
    ]
