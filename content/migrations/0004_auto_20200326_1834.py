# Generated by Django 3.0.4 on 2020-03-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0003_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(max_length=30, unique=True),
        ),
    ]
