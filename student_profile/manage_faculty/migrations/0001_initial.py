# Generated by Django 5.0 on 2024-05-21 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementsFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('achievement_certificate', models.ImageField(blank=True, null=True, upload_to='achievement_certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='InterestsFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=100)),
                ('interest_certificate', models.ImageField(blank=True, null=True, upload_to='interest_certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='LanguagesFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('proficiency_level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('language_certificate', models.ImageField(blank=True, null=True, upload_to='language_certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInfoFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField(max_length=500)),
                ('aadhar_front', models.ImageField(blank=True, null=True, upload_to='')),
                ('aadhar_back', models.ImageField(blank=True, null=True, upload_to='')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='SkillsFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
                ('proficiency_level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('skill_certificate', models.ImageField(blank=True, null=True, upload_to='skill_certificates/')),
            ],
        ),
    ]