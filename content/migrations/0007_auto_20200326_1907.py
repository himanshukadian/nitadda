# Generated by Django 3.0.4 on 2020-03-26 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0006_subject_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(editable=False, max_length=30, unique=True),
        ),
    ]
