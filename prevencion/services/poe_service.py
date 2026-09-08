"""
Servicio del Asistente Virtual "Sonia".

Este modulo centraliza la logica para generar las respuestas del chat.
Por ahora responde con un asistente simple basado en reglas para que la
funcionalidad quede operativa de punta a punta (UI <-> backend).

Para conectar la API real de Poe (o la que se decida usar):
  1. Agregar la API key como variable de entorno (nunca hardcodeada).
  2. Reemplazar el cuerpo de `obtener_respuesta_sonia` por la llamada HTTP
     correspondiente, manteniendo la misma firma de funcion para no romper
     la vista que la consume (prevencion/views.py -> asistente_virtual_mensaje).
"""

import os

# Ejemplo de donde iria la API key real cuando se conecte el servicio:
# POE_API_KEY = os.environ.get("POE_API_KEY")

RESPUESTAS_FRECUENTES = {
    "hola": "Hola! Soy Sonia, tu asistente virtual de salud mamaria. En que puedo ayudarte hoy?",
    "autoexamen": (
        "El autoexamen mamario se recomienda hacerlo una vez al mes, idealmente "
        "unos dias despues de terminada la menstruacion. Revisa forma, textura y "
        "posibles bultos. Ante cualquier cambio, consulta con tu medico."
    ),
    "mamografia": (
        "La mamografia es el examen de referencia para la deteccion temprana. "
        "Se recomienda generalmente desde los 40 anios, o antes si existen "
        "antecedentes familiares. Tu medico puede indicarte la frecuencia adecuada."
    ),
}


def obtener_respuesta_sonia(mensaje_usuario: str) -> str:
    """
    Genera una respuesta para el mensaje del usuario.

    Args:
        mensaje_usuario: texto enviado por el paciente en el chat.

    Returns:
        Texto de respuesta de Sonia.
    """
    texto = mensaje_usuario.lower()

    for palabra_clave, respuesta in RESPUESTAS_FRECUENTES.items():
        if palabra_clave in texto:
            return respuesta

    return (
        "Gracias por tu mensaje. Este asistente todavia esta en configuracion: "
        "pronto podre responder con IA en base a tu consulta. Por ahora, te "
        "recomiendo revisar el Modulo Educativo o consultar directamente con "
        "tu especialista ante cualquier duda urgente."
    )
