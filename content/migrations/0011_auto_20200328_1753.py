# Generated by Django 3.0.4 on 2020-03-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0010_auto_20200328_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, unique=True),
        ),
    ]
