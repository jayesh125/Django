# Generated by Django 5.0 on 2024-06-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_users', '0017_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='f2b766', max_length=6),
        ),
    ]