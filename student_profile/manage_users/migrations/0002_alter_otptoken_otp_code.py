# Generated by Django 5.0 on 2024-05-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='8ab317', max_length=6),
        ),
    ]