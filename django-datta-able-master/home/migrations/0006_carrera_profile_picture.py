# Generated by Django 4.2.9 on 2024-04-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_userprofile_carrera'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrera',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/carrera/'),
        ),
    ]
