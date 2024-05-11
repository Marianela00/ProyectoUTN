
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from enum import Enum


class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    info = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/carrera/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Materia(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    info = models.TextField()
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materias_asignadas')
    enlace_zoom = models.URLField(blank=True, null=True)  # Campo para el enlace de Zoom
    profile_picture = models.ImageField(upload_to='profile_pictures/carrera/materia', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class MaterialEducativo(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materiales_educativos')
    nombreMaterial = models.CharField(max_length=100, null=True)
    archivo = models.FileField(upload_to='materiales/', blank=True, null=True)
    
    def __str__(self):
        return f"Material Educativo de {self.materia.nombre}"


class DiaSemana(Enum):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miércoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    # Agrega más días según sea necesario

class HorarioClase(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='horarios_clase')
    dia_semana = models.CharField(max_length=10, choices=[(dia.name, dia.value) for dia in DiaSemana])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.hora_inicio} a {self.hora_fin}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class CanalPrivado(models.Model):
    usuario1 = models.ForeignKey(User, related_name='canales_usuario1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(User, related_name='canales_usuario2', on_delete=models.CASCADE)

class Mensaje(models.Model):
    canal = models.ForeignKey(CanalPrivado, related_name='mensajes', on_delete=models.CASCADE, null=True)
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    