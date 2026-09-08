import json
import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PreguntaEducativa, AnalisisEcografia
from .services import poe_service

def registro_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')

        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya existe. Intenta con otro.')
            return redirect('registro')

        nuevo_usuario = User.objects.create_user(username=usuario, email=correo, password=clave)
        nuevo_usuario.save()

        login(request, nuevo_usuario)
        return redirect('inicio')

    return render(request, 'prevencion/registro.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')

        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('iniciar_sesion')

    return render(request, 'prevencion/iniciar_sesion.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


@login_required(login_url='iniciar_sesion')
def inicio(request):
    return render(request, 'prevencion/inicio.html')


@login_required(login_url='iniciar_sesion')
def educativo_menu(request):
    return render(request, 'prevencion/menu_educativo.html')


@login_required(login_url='iniciar_sesion')
def educativo_sesion(request, tipo_sesion):
    nombres_sesion = {
        'S1': 'Sesión 1: Mitos vs Realidades',
        'S2': 'Sesión 2: Preguntas Clave',
        'S3': 'Sesión 3: Verdadero o Falso',
    }
    
    preguntas = PreguntaEducativa.objects.filter(sesion=tipo_sesion)
    nombre = nombres_sesion.get(tipo_sesion, 'Sesión Educativa')
    
    context = {
        'preguntas': preguntas,
        'nombre_sesion': nombre,
        'codigo_sesion': tipo_sesion
    }
    return render(request, 'prevencion/sesion_educativa.html', context)


@login_required(login_url='iniciar_sesion')
def analisis_imagen(request):
    """
    Permite al paciente subir una imagen (ecografía/mamografía) y guarda el
    registro del análisis. El cálculo de riesgo es un placeholder por ahora:
    aquí es donde se debe conectar el modelo de IA real (ver services/poe_service.py).
    """
    resultado = None

    if request.method == 'POST':
        imagen = request.FILES.get('imagen_original')

        if not imagen:
            messages.error(request, 'Debes seleccionar una imagen antes de continuar.')
            return redirect('analisis_imagen')

        # --- PLACEHOLDER: reemplazar por la llamada al modelo de IA real ---
        porcentaje_riesgo = round(random.uniform(5, 40), 1)
        if porcentaje_riesgo < 15:
            rango_alerta = 'Verde'
        elif porcentaje_riesgo < 30:
            rango_alerta = 'Amarillo'
        else:
            rango_alerta = 'Rojo'
        # --------------------------------------------------------------

        analisis = AnalisisEcografia.objects.create(
            usuario=request.user,
            imagen_original=imagen,
            porcentaje_riesgo=porcentaje_riesgo,
            rango_alerta=rango_alerta,
        )
        resultado = analisis
        messages.success(request, 'Imagen analizada correctamente.')

    historial = AnalisisEcografia.objects.filter(usuario=request.user).order_by('-fecha_analisis')[:5]

    context = {
        'resultado': resultado,
        'historial': historial,
    }
    return render(request, 'prevencion/analisis_imagen.html', context)


@login_required(login_url='iniciar_sesion')
def asistente_virtual(request):
    return render(request, 'prevencion/asistente_virtual.html')


@login_required(login_url='iniciar_sesion')
@require_POST
def asistente_virtual_mensaje(request):
    """
    Endpoint AJAX que recibe el mensaje del usuario y devuelve la respuesta
    de Sonia. Delega la generación de la respuesta a services/poe_service.py,
    que hoy responde con un mensaje de referencia hasta que se conecte la API real.
    """
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        data = {}

    mensaje_usuario = (data.get('mensaje') or '').strip()

    if not mensaje_usuario:
        return JsonResponse({'error': 'Mensaje vacío.'}, status=400)

    respuesta = poe_service.obtener_respuesta_sonia(mensaje_usuario)

    return JsonResponse({'respuesta': respuesta})