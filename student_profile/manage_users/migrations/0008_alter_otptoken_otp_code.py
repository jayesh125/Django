# Generated by Django 5.0 on 2024-05-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_users', '0007_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='5929c6', max_length=6),
        ),
    ]