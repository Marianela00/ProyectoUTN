# Generated by Django 4.2.9 on 2024-04-05 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0011_materia_enlace_zoom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materia',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias_asignadas', to=settings.AUTH_USER_MODEL),
        ),
    ]