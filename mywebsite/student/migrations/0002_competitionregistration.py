# Generated by Django 3.1.1 on 2020-11-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
    ]
