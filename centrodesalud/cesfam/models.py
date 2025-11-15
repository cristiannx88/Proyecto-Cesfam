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
    


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cargo'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('licencia', 'Licencia'),
        ('vacaciones', 'Vacaciones'),
    ]

    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Asignar rol Administrador automáticamente a superusuarios
        if self.is_superuser:
            try:
                rol_admin = Rol.objects.get(nombre_rol="Administrador")
                self.id_rol = rol_admin
            except Rol.DoesNotExist:
                # Evita error si aún no creaste el rol
                pass

        super().save(*args, **kwargs)



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
    TIPOS_PERMISO = [
        ('Administrativo', 'Día Administrativo - Trámites personales'),
        ('Libre', 'Día Libre - Compensación por horas extras'),
    ]

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
        ('Cancelado', 'Cancelado'),
    ]

    solicitante = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='solicitudes_permiso'
    )

    tipo_permiso = models.CharField(max_length=50, choices=TIPOS_PERMISO)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    documento_respaldo = models.FileField(upload_to='permisos/', blank=True, null=True)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    revisado_por_direccion = models.CharField(max_length=100, null=True, blank=True)
    fecha_revision_direccion = models.DateTimeField(null=True, blank=True)
    revisado_por_subdireccion = models.CharField(max_length=100, null=True, blank=True)
    fecha_revision_subdireccion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'solicitud_permiso'

    def __str__(self):
        return f"{self.tipo_permiso} ({self.estado})"
    

    def estado_detallado(self):
        if self.estado.lower() == 'aprobado':
            detalles = []
            if self.revisado_por_direccion and self.fecha_revision_direccion:
                detalles.append(f"Dirección ({self.fecha_revision_direccion.strftime('%d/%m/%Y %H:%M')})")
            if self.revisado_por_subdireccion and self.fecha_revision_subdireccion:
                detalles.append(f"Subdirección ({self.fecha_revision_subdireccion.strftime('%d/%m/%Y %H:%M')})")
            if detalles:
                return "Aprobado por " + " y ".join(detalles)
            else:
                return "Aprobado"

        elif self.estado.lower() == 'rechazado':
            return "Solicitud Rechazada"

        elif self.estado.lower() == 'cancelado':
            return "Solicitud cancelada por el funcionario"

        else:  # Pendiente
            if self.revisado_por_direccion and not self.revisado_por_subdireccion:
                return "Pendiente: Falta revisión Subdirección"
            elif self.revisado_por_subdireccion and not self.revisado_por_direccion:
                return "Pendiente: Falta revisión Dirección"
            else:
                return "Pendiente (sin revisión)"

    @property
    def dias_solicitados(self):
        """Calcula automáticamente la cantidad de días solicitados"""
        return (self.fecha_fin - self.fecha_inicio).days + 1




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
    