


# Importa las clases y funciones necesarias de varios módulos de Django:
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404   # Importa las funciones render y redirect de django.shortcuts
from admin_datta.forms import (  # Importa varios formularios del módulo admin_datta.forms
    RegistrationForm, 
    LoginForm, 
    UserPasswordChangeForm, 
    UserPasswordResetForm, 
    UserSetPasswordForm
)
from django.contrib.auth.views import (  # Importa vistas de autenticación de Django
    LoginView, 
    PasswordChangeView, 
    PasswordResetConfirmView, 
    PasswordResetView
)
from django.db.models import Q  # Añade esta línea al principio de tu archivo views.py
from django.contrib.auth import logout  # Importa la función logout de django.contrib.auth

from django.contrib.auth.decorators import login_required  # Importa el decorador login_required de django.contrib.auth.decorators

from .models import *  # Importa todos los modelos definidos en el archivo actual
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from django.core.exceptions import ObjectDoesNotExist  # Importa la excepción ObjectDoesNotExist
from django.utils import timezone
from .models import Materia
from django.contrib import messages
from datetime import datetime, timedelta



@login_required
def index(request):
    # Obtén el usuario actual
    current_user = request.user
    
    # Obtén los superusuarios en línea que iniciaron sesión en los últimos 5 minutos, excluyendo al usuario actual
    superusers_online = User.objects.filter(
        is_superuser=True,  # Filtrar solo los superusuarios
        last_login__gte=timezone.now() - timezone.timedelta(minutes=30)
    ).exclude(id=current_user.id).order_by('-last_login')

    # Obtén el perfil de usuario del alumno actual
    try:
        user_profile = request.user.userprofile
    except ObjectDoesNotExist:
        user_profile = None

    carrera_asignada = None
    # Obtén la materia asignada al alumno (si la hay)
    materia_asignada = None
    if user_profile:
        try:
            # Busca la materia asignada al alumno
            carrera_asignada = user_profile.carrera
            materia_asignada = Materia.objects.get(carrera=user_profile.carrera)
        except ObjectDoesNotExist:
            pass

    context = {
        'segment': 'index',
        'superusers_online': superusers_online,
        'user_profile': user_profile,
        'materia_asignada': materia_asignada,
        'carrera_asignada': carrera_asignada,  # Pasar la carrera asignada al contexto
    }

    return render(request, "pages/index.html", context)





# Define la vista tables
def tables(request):
    context = {
        'segment': 'tables'  # Define un contexto con la clave 'segment' con valor 'tables'
    }
    return render(request, "pages/dynamic-tables.html", context)  # Renderiza el template 'pages/dynamic-tables.html' con el contexto dado y devuelve la respuesta


@login_required
def edit_profile(request):
    user = request.user

    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_profile:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            if profile_form:
                if user_profile:
                    profile_form.save()
                else:
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
            return redirect('profile')  # Cambia 'perfil' por el nombre de la URL de la página de perfil del usuario
    else:
        user_form = UserForm(instance=user)
        if user_profile:
            profile_form = UserProfileForm(instance=user_profile)
        else:
            profile_form = UserProfileForm()
    
    return render(request, 'pages/profile.html', {'user': user, 'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile})




@login_required
def bc_carreras(request, materia_id=None):
    try:
        # Obtener el perfil del usuario
        user_profile = request.user.userprofile
        
        # Verificar si el usuario tiene una carrera asociada en su perfil
        if user_profile.carrera:
            # Obtener todas las materias asociadas a la carrera del usuario
            materias = Materia.objects.filter(carrera=user_profile.carrera)
            
            # Si se proporciona un ID de materia, obtener los detalles de esa materia
            if materia_id:
                materia = get_object_or_404(Materia, id=materia_id)
                return render(request, 'pages/components/carreras.html', {'materias': materias, 'materia': materia})
            
            # Si no se proporciona un ID de materia, solo mostrar la lista de materias
            return render(request, 'pages/components/carreras.html', {'materias': materias})
        else:
            # Si el usuario no tiene una carrera asociada, manejar este caso según tus necesidades
            if request.user.userprofile:
                # El usuario ya tiene un perfil, redirigir a la página de edición de perfil
                return redirect('edit_user')
            else:
                # El usuario no tiene un perfil, mostrar un mensaje para que edite su perfil
                messages.warning(request, 'Por favor, complete su perfil antes de continuar.')
                return redirect('edit_user')
    except ObjectDoesNotExist:
        # Manejar el caso donde UserProfile no existe para el usuario
        # Puedes redirigir al usuario a completar su perfil o mostrar un mensaje de error
        messages.warning(request, 'Por favor, complete su perfil antes de continuar.')
        return redirect('edit_user')  # Redirigir a la página para completar el perfil, o a donde necesites
 
    
def mostrar_calendario(request):
    # Obtener todos los horarios de clase
    
    return render(request, 'pages/components/calendario.html')



def get_horarios_clase(request):
    # Obtener todos los horarios de clase
    horarios_clase = HorarioClase.objects.all()
    
    # Definir los días de la semana
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Lista para almacenar los eventos de clase
    eventos_clase = []

    # Iterar sobre los horarios de clase
    for horario in horarios_clase:
        # Obtener el índice del día de la semana para este horario
        indice_dia = dias_semana.index(horario.dia_semana.lower())
        
        # Calcular la fecha del primer día de la semana actual
        fecha_dia_semana = fecha_actual - timedelta(days=fecha_actual.weekday() - indice_dia)

        # Agregar eventos para cada día de la semana a lo largo del año
        for i in range(52):
            # Construir un diccionario para cada horario de clase
            evento = {
                'id': horario.id,
                'title': horario.materia.nombre,
                'start': (fecha_dia_semana + timedelta(weeks=i)).strftime('%Y-%m-%dT') + str(horario.hora_inicio),
                'end': (fecha_dia_semana + timedelta(weeks=i)).strftime('%Y-%m-%dT') + str(horario.hora_fin),
            }
            # Agregar el evento a la lista de eventos
            eventos_clase.append(evento)

    # Devolver la lista de eventos en formato JSON
    return JsonResponse(eventos_clase, safe=False)


# notifications




@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        destinatario_username = request.POST.get('destinatario')
        contenido = request.POST.get('contenido')

        destinatario = User.objects.get(username=destinatario_username)
        remitente = request.user

        # Buscar o crear el canal entre el remitente y el destinatario
        canal, creado = CanalPrivado.objects.get_or_create(usuario1=remitente, usuario2=destinatario)

        # Crear el mensaje en el canal correspondiente
        Mensaje.objects.create(canal=canal, remitente=remitente, contenido=contenido)

        return redirect('bandeja_entrada')

    return render(request, 'pages/components/bandeja_entrada.html')

@login_required
def responder_y_ver_mensaje(request, mensaje_id=None):
    if mensaje_id:
        # Si se proporciona un mensaje_id, significa que estamos respondiendo a un mensaje existente
        mensaje = get_object_or_404(Mensaje, id=mensaje_id)
        
        # Verificar si el usuario actual es el remitente o el destinatario del mensaje
        if request.user != mensaje.remitente and request.user not in [mensaje.canal.usuario1, mensaje.canal.usuario2]:
            # Si el usuario actual no es el remitente ni el destinatario, redirigirlo a la bandeja de entrada
            return redirect('bandeja_entrada')
        
        if request.method == 'POST':
            contenido_respuesta = request.POST.get('contenido')
            # Enviar la respuesta al remitente original del mensaje
            Mensaje.objects.create(canal=mensaje.canal, remitente=request.user, contenido=contenido_respuesta)
            return redirect('bandeja_entrada')

        return render(request, 'pages/components/ver_y_responder_mensaje.html', {'mensaje': mensaje})
    else:
        # Si no se proporciona un mensaje_id, significa que estamos creando un nuevo mensaje de respuesta
        if request.method == 'POST':
            contenido_respuesta = request.POST.get('contenido')
            mensaje_id = request.POST.get('mensaje_id')
            mensaje = get_object_or_404(Mensaje, id=mensaje_id)
            if request.user != mensaje.remitente and request.user not in [mensaje.canal.usuario1, mensaje.canal.usuario2]:
                return redirect('bandeja_entrada')
            Mensaje.objects.create(canal=mensaje.canal, remitente=request.user, contenido=contenido_respuesta)
            return redirect('bandeja_entrada')

        return render(request, 'pages/components/ver_y_responder_mensaje.html')






@login_required
def bandeja_entrada(request):
    # Obtener todos los mensajes en los canales compartidos por el usuario actual
    canales_del_usuario = CanalPrivado.objects.filter(Q(usuario1=request.user) | Q(usuario2=request.user))
    mensajes = Mensaje.objects.filter(canal__in=canales_del_usuario)
    
    # Obtener los usuarios con los que el usuario actual comparte canales
    usuarios_en_canales = set()
    for canal in canales_del_usuario:
        if canal.usuario1 != request.user:
            usuarios_en_canales.add(canal.usuario1)
        if canal.usuario2 != request.user:
            usuarios_en_canales.add(canal.usuario2)

    # Obtener todos los usuarios
    usuarios = User.objects.all()
    
    return render(request, 'pages/components/bandeja_entrada.html', {'mensajes': mensajes, 'usuarios_en_canales': usuarios_en_canales, 'usuarios': usuarios})




