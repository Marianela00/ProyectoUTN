# Importa las clases y funciones necesarias de varios módulos de Django:
from django.contrib import admin  # Importa la interfaz de administración de Django
from django.urls import include, path  # Importa las funciones include y path para definir patrones de URL
from rest_framework.authtoken.views import obtain_auth_token  # <-- NEW: Importa la vista obtain_auth_token para autenticación con token

# Define una lista llamada urlpatterns, que contiene varios patrones de URL.
urlpatterns = [
    path('', include('home.urls')),  # Vincula las URL definidas en la aplicación "home"
    path("admin/", admin.site.urls),  # Vincula la interfaz de administración de Django
    path("", include('admin_datta.urls')),  # Vincula las URL definidas en la aplicación "admin_datta"
    path('', include('django_dyn_dt.urls')),  # <-- NEW: Vincula las URL definidas en la aplicación "django_dyn_dt"   
]

# Lazy-load on routing is needed
# Durante la primera carga, API aún no está generada
# Intenta agregar dos patrones de URL adicionales para API y autenticación JWT.
# Si alguna excepción ocurre, se captura y se ignora.
try:
    urlpatterns.append(path("api/", include("api.urls")))  # Vincula las URL definidas en la aplicación "api"
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))  # Vincula la vista obtain_auth_token para autenticación JWT
except:
    pass  # Si ocurre alguna excepción, ignórala y continúa con la ejecución del código
