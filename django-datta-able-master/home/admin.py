# Importa las clases y funciones necesarias de varios módulos de Django:
from django.contrib import admin  # Importa la interfaz de administración de Django
from django.apps import apps  # Importa la función apps del módulo django.apps

# Obtiene todos los modelos de la aplicación 'home'
app_models = apps.get_app_config('home').get_models()

# Itera sobre cada modelo obtenido
for model in app_models:
    try:
        admin.site.register(model)  # Intenta registrar el modelo en la interfaz de administración
    except Exception:
        pass  # Si ocurre alguna excepción, ignórala y continúa con la ejecución del bucle
