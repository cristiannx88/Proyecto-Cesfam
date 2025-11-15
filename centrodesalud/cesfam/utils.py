#Archivo para los logs

from .models import LogActividad
from django.utils import timezone

def registrar_log(usuario, accion, tabla=None, objeto_id=None, request=None, detalles=None):
    ip = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    LogActividad.objects.create(
        id_usuario=usuario,
        accion=accion,
        tabla_afectada=tabla,
        id_objeto=objeto_id,
        ip_address=ip,
        detalles=detalles,
        fecha_hora=timezone.now()
    )
