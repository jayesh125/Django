# Generated by Django 5.0 on 2024-06-02 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_admin', '0007_message_courses_message_specializations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='semester',
        ),
        migrations.AddField(
            model_name='student',
            name='enrollment_status',
            field=models.CharField(choices=[('enrolled', 'Enrolled'), ('completed', 'Completed'), ('dropped', 'Dropped')], default='...', max_length=50),
        ),
        migrations.DeleteModel(
            name='Enrollment',
        ),
        migrations.DeleteModel(
            name='Semester',
        ),
    ]
