# Generated by Django 5.0 on 2024-05-31 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_users', '0013_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='cb38a2', max_length=6),
        ),
    ]
