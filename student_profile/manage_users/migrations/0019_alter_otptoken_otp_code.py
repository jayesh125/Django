# Generated by Django 5.0 on 2024-06-04 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_users', '0018_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='0c70e3', max_length=6),
        ),
    ]