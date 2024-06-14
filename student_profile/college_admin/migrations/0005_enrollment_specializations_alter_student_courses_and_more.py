# Generated by Django 5.0 on 2024-05-28 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college_admin', '0004_student_courses_student_specializations'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='specializations',
            field=models.ManyToManyField(blank=True, to='college_admin.specialization'),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(blank=True, to='college_admin.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='specializations',
            field=models.ManyToManyField(blank=True, to='college_admin.specialization'),
        ),
    ]
