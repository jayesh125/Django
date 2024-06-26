# Generated by Django 5.0 on 2024-05-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('date_posted', models.DateField()),
                ('image', models.ImageField(upload_to='blog_images/')),
                ('content', models.TextField()),
            ],
        ),
    ]
