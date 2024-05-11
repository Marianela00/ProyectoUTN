# Importa las clases y funciones necesarias de varios módulos de Django:
from django.urls import path  # Importa la función path para definir patrones de URL
from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación de Django con un alias "auth_views"
from django.conf import settings
from django.conf.urls.static import static  # Importa la función static para servir archivos estáticos

# Importa las vistas definidas en el archivo actual
from . import views  

# Define una lista llamada urlpatterns, que contiene varios patrones de URL.
urlpatterns = [
    path('', views.index,  name='index'),  # Define un patrón de URL vacío que dirige a la vista 'index' definida en 'views.py'
    path('tables/', views.tables, name='tables'),  # Define un patrón de URL 'tables/' que dirige a la vista 'tables' definida en 'views.py'
    path('profile/', views.edit_profile, name='edit_user'),
    path('bc_carreras/', views.bc_carreras, name='bc_carreras'),  # Ruta para la vista bc_carreras
    path('bc_carreras/<int:materia_id>/', views.bc_carreras, name='detalle_materia'),
    path('mostrar_calendario/', views.mostrar_calendario, name='mostrar_calendario'),
    path('get-horarios-clase/', views.get_horarios_clase, name='get_horarios_clase'),
    path('bandeja-entrada/', views.bandeja_entrada, name='bandeja_entrada'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensaje/<int:mensaje_id>/', views.responder_y_ver_mensaje, name='responder_y_ver_mensaje'),
    
]

# Configuración para servir archivos de medios estáticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



