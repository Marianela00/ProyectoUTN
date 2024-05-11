# Generated by Django 4.2.9 on 2024-04-04 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_materia_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='material_educativo',
        ),
        migrations.CreateModel(
            name='MaterialEducativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(blank=True, null=True, upload_to='materiales/')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiales_educativos', to='home.materia')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioClase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(max_length=10)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_clase', to='home.materia')),
            ],
        ),
    ]
