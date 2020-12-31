# Generated by Django 3.1.2 on 2020-11-04 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('dates', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSection',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phoneno', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=255)),
                ('profession', models.CharField(max_length=255)),
                ('years', models.CharField(max_length=255)),
                ('hobbies', models.CharField(max_length=255)),
                ('areaofinterest', models.CharField(max_length=255)),
                ('socialprof', models.CharField(max_length=255)),
                ('yourself', models.CharField(max_length=255)),
                ('keylearn', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('course_name', models.CharField(max_length=255)),
                ('batch_count', models.IntegerField()),
                ('course_details', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('medium', models.CharField(max_length=255)),
                ('days', models.CharField(max_length=255)),
                ('key_learnings', models.CharField(max_length=255)),
                ('age_group', models.CharField(max_length=255)),
                ('prerequisites', models.CharField(max_length=255)),
                ('things', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOverview',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=255)),
                ('courseSubtitle', models.CharField(max_length=255)),
                ('duration', models.IntegerField(default=16)),
                ('age', models.IntegerField()),
                ('batch', models.IntegerField()),
                ('mediumOfInstruct', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=255)),
                ('courseReq', models.CharField(max_length=255)),
                ('topics', models.CharField(max_length=255)),
                ('payment', models.IntegerField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('accountNo', models.CharField(max_length=255)),
                ('accountType', models.CharField(max_length=255)),
                ('ifsc', models.CharField(max_length=255)),
                ('bankName', models.CharField(max_length=255)),
                ('branch', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]