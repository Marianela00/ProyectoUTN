from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from api.views import CarreraView, MateriaView

urlpatterns = [
    re_path("carrera/((?P<pk>\d+)/)?", csrf_exempt(CarreraView.as_view())),
    re_path("materia/((?P<pk>\d+)/)?", csrf_exempt(MateriaView.as_view())),
]
