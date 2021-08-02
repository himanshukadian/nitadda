# Generated by Django 3.0.4 on 2021-08-02 22:38

import content.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=30, unique=True)),
                ('abbreviation', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('slug', models.SlugField(editable=False, max_length=30, unique=True)),
                ('duration', models.IntegerField(default=4)),
                ('no_of_semesters', models.IntegerField(default=8)),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Paper_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_cnt', models.IntegerField(default=0)),
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
                ('slug', models.SlugField(editable=False, max_length=30, unique=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=300)),
                ('note_pdf', models.FileField(blank=True, default=None, null=True, upload_to=content.models.get_note_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('is_approved', models.BooleanField(default=False)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.College', verbose_name='College')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course', verbose_name='Course')),
                ('reports', models.ManyToManyField(related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Subject', verbose_name='Subject')),
                ('upvotes', models.ManyToManyField(related_name='upvotes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Paper',
            fields=[
                ('paper_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=300)),
                ('batch_year', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('exam', models.CharField(max_length=20)),
                ('exam_type', models.CharField(choices=[('T', 'Theory'), ('P', 'Practical')], default='T', max_length=1)),
                ('paper_pdf', models.FileField(blank=True, default=None, null=True, upload_to=content.models.get_paper_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('is_approved', models.BooleanField(default=False)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.College', verbose_name='College')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course', verbose_name='Course')),
                ('reports', models.ManyToManyField(related_name='paper_reports', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Subject', verbose_name='Subject')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=300)),
                ('flink', models.CharField(blank=True, max_length=300)),
                ('upload_type', models.CharField(choices=[('L', 'Link'), ('P', 'PDF')], default='L', max_length=1)),
                ('slug', models.SlugField(editable=False, max_length=30, unique=True)),
                ('book_pdf', models.FileField(blank=True, default=None, null=True, upload_to=content.models.get_book_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('is_approved', models.BooleanField(default=False)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.College', verbose_name='College')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course', verbose_name='Course')),
                ('reports', models.ManyToManyField(related_name='book_reports', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Subject', verbose_name='Subject')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=10000)),
                ('date', models.DateTimeField()),
                ('image', models.ImageField(default='download.jpg', upload_to='blogs/')),
                ('is_approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Provider')),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.College', verbose_name='College')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course', verbose_name='Course')),
                ('reports', models.ManyToManyField(blank=True, related_name='blog_reports', to=settings.AUTH_USER_MODEL)),
                ('upvotes', models.ManyToManyField(blank=True, related_name='blog_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
