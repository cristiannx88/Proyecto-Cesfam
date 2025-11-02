from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractUser):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Documento(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('archivado', 'Archivado'),
    ]
    
    TIPO_CHOICES = [
        ('protocolo', 'Protocolo'),
        ('circular', 'Circular'),
        ('manual', 'Manual'),
        ('informe', 'Informe'),
        ('otro', 'Otro'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    id_usuario_autor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='documentos')
    ruta_archivo = models.FileField(upload_to='documentos/%Y/%m/')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    class Meta:
        db_table = 'documento'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return self.titulo

class Comunicado(models.Model):
    TIPO_CHOICES = [
        ('urgente', 'Urgente'),
        ('importante', 'Importante'),
        ('normal', 'Normal'),
        ('info', 'Informativo'),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    fecha_programada = models.DateTimeField(blank=True, null=True)
    id_autor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='comunicados')
    destacado = models.BooleanField(default=False)
    archivo_adjunto = models.FileField(upload_to='comunicados/%Y/%m/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='normal')  # <-- agregado

    class Meta:
        db_table = 'comunicado'
        verbose_name = 'Comunicado'
        verbose_name_plural = 'Comunicados'
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo


class Calendario(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('reunion', 'Reunión'),
        ('capacitacion', 'Capacitación'),
        ('feriado', 'Feriado'),
        ('actividad', 'Actividad'),
        ('otro', 'Otro'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo_evento = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES)
    lugar = models.CharField(max_length=200, blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='eventos_creados')
    
    class Meta:
        db_table = 'calendario'
        verbose_name = 'Evento'
        verbose_name_plural = 'Calendario'
        ordering = ['fecha_inicio']
    
    def __str__(self):
        return self.titulo

class SolicitudPermiso(models.Model):
    TIPO_PERMISO_CHOICES = [
        ('administrativo', 'Día Administrativo'),
        ('vacaciones', 'Vacaciones'),
        ('permiso_personal', 'Permiso Personal'),
        ('permiso_medico', 'Permiso Médico'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    funcionario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='solicitudes_permiso')
    tipo_permiso = models.CharField(max_length=50, choices=TIPO_PERMISO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    revisado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='permisos_revisados')
    fecha_revision = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'solicitud_permiso'
        verbose_name = 'Solicitud de Permiso'
        verbose_name_plural = 'Solicitudes de Permiso'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"{self.funcionario} - {self.tipo_permiso} ({self.estado})"

class LicenciaMedica(models.Model):
    TIPO_LICENCIA_CHOICES = [
        ('maternal', 'Maternal'),
        ('enfermedad', 'Enfermedad Común'),
        ('accidente_trabajo', 'Accidente de Trabajo'),
        ('accidente_trayecto', 'Accidente de Trayecto'),
        ('prorroga', 'Prórroga'),
    ]
    
    funcionario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='licencias_medicas')
    tipo_licencia = models.CharField(max_length=50, choices=TIPO_LICENCIA_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_reposo = models.IntegerField()
    numero_folio = models.CharField(max_length=50, unique=True)
    archivo_licencia = models.FileField(upload_to='licencias/%Y/%m/')
    fecha_carga = models.DateTimeField(default=timezone.now)
    cargado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='licencias_cargadas')
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'licencia_medica'
        verbose_name = 'Licencia Médica'
        verbose_name_plural = 'Licencias Médicas'
        ordering = ['-fecha_carga']
    
    def __str__(self):
        return f"Licencia {self.numero_folio} - {self.funcionario}"

class LogActividad(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='logs')
    accion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(default=timezone.now)
    tabla_afectada = models.CharField(max_length=50, blank=True, null=True)
    id_objeto = models.IntegerField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    detalles = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'log_actividad'
        verbose_name = 'Log de Actividad'
        verbose_name_plural = 'Logs de Actividad'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.id_usuario} - {self.accion} ({self.fecha_hora})"
