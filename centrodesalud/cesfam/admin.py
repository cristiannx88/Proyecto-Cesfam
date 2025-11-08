from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Rol,
    Usuario,
    Documento,
    Comunicado,
    Calendario,
    SolicitudPermiso,
    LicenciaMedica,
    LogActividad,
    Cargo,
    Departamento
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol', 'descripcion')
    search_fields = ('nombre_rol',)


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'rut',
        'telefono', 'cargo', 'departamento', 'id_rol', 'estado',
        'is_staff', 'is_superuser'
    )
    list_filter = ('estado', 'id_rol', 'cargo', 'departamento', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut', 'telefono')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': (
                'first_name', 'last_name', 'email', 'rut',
                'telefono', 'cargo', 'departamento', 'observaciones'
            )
        }),
        ('Permisos y Rol', {
            'fields': (
                'id_rol', 'estado',
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'rut',
                'telefono', 'cargo', 'departamento', 'id_rol', 'password1', 'password2',
                'is_staff', 'is_superuser'
            ),
        }),
    )


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'id_usuario_autor', 'fecha_subida', 'estado')
    list_filter = ('tipo', 'estado', 'fecha_subida')
    search_fields = ('titulo', 'descripcion', 'id_usuario_autor__username')


@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id_autor', 'fecha_publicacion', 'destacado')
    list_filter = ('destacado', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido', 'id_autor__username')


@admin.register(Calendario)
class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_evento', 'fecha_inicio', 'fecha_fin', 'creado_por')
    list_filter = ('tipo_evento', 'fecha_inicio')
    search_fields = ('titulo', 'descripcion', 'lugar', 'creado_por__username')

from django.contrib import admin
from .models import SolicitudPermiso

@admin.register(SolicitudPermiso)
class SolicitudPermisoAdmin(admin.ModelAdmin):
    list_display = ('tipo_permiso', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_solicitud')



@admin.register(LicenciaMedica)
class LicenciaMedicaAdmin(admin.ModelAdmin):
    list_display = ('numero_folio', 'funcionario', 'tipo_licencia', 'fecha_inicio', 'fecha_fin', 'dias_reposo', 'cargado_por')
    list_filter = ('tipo_licencia', 'fecha_inicio', 'fecha_fin')
    search_fields = ('funcionario__username', 'numero_folio', 'cargado_por__username')


@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'accion', 'tabla_afectada', 'id_objeto', 'fecha_hora', 'ip_address')
    list_filter = ('tabla_afectada', 'fecha_hora')
    search_fields = ('id_usuario__username', 'accion', 'detalles')
