# Generated by Django 3.0.4 on 2020-03-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0004_auto_20200326_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(editable=False, max_length=30, unique=True),
        ),
    ]
