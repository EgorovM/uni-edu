# Generated by Django 3.1 on 2020-08-30 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_delete_notification'),
        ('course', '0005_course_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('students', models.ManyToManyField(blank=True, to='student.Student')),
            ],
        ),
    ]