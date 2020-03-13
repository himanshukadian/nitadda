# Generated by Django 3.0.4 on 2020-03-11 10:56

import content.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Note_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to='content.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=300)),
                ('note_pdf', models.FileField(blank=True, default=None, null=True, upload_to=content.models.get_path,
                                              validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to='content.Course', verbose_name='Course')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              to='content.Subject', verbose_name='Subject')),
            ],
        ),
    ]
