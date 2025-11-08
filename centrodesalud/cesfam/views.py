from django.contrib.auth.decorators import login_required
from .models import Documento, Comunicado, Usuario, LicenciaMedica, SolicitudPermiso, Calendario
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ComunicadoForm, DocumentoForm, RegistroForm, SolicitudPermisoForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone
from django.contrib.auth import login, authenticate


@login_required
def home(request):
    """Vista para la página de inicio"""
    context = {
        'total_documentos': Documento.objects.count(),
        'total_funcionarios': Usuario.objects.count(),
        'total_permisos': SolicitudPermiso.objects.count(),
        'comunicados_recientes': Comunicado.objects.all()[:5]
    }
    return render(request, 'cesfam/home.html', context)


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado correctamente. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()
    return render(request, 'cesfam/registro.html', {'form': form})



@login_required
def documentos_list(request):
    documentos = Documento.objects.all().order_by('-fecha_subida')

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.id_usuario_autor = request.user
            documento.save()
            messages.success(request, 'Documento subido correctamente.')
            return redirect('documentos_list')
        else:
            messages.error(request, 'Error al subir el documento. Revisa los campos.')
    else:
        form = DocumentoForm()

    return render(request, 'cesfam/documentos_list.html', {
        'form': form,
        'documentos': documentos,
    })



@login_required
def comunicados_list(request):
    """Vista para listar y crear comunicados"""
    comunicados = Comunicado.objects.all().order_by('-fecha_publicacion')

    if request.method == 'POST':
        form = ComunicadoForm(request.POST, request.FILES)
        if form.is_valid():
            comunicado = form.save(commit=False)
            comunicado.id_autor = request.user  # El superusuario actual
            comunicado.save()
            messages.success(request, 'Comunicado publicado correctamente.')
            return redirect('comunicados_list')
        else:
            messages.error(request, 'Error al publicar el comunicado. Revisa los campos.')
    else:
        form = ComunicadoForm()

    return render(request, 'cesfam/comunicados_list.html', {
        'form': form,
        'comunicados': comunicados,
    })



@login_required
def calendario_view(request):
    """Vista principal del calendario"""
    year = timezone.now().year
    eventos = Calendario.objects.all().order_by('fecha_inicio')
    return render(request, 'cesfam/calendario.html', {'year': year, 'eventos': eventos})


@login_required
def eventos_json(request):
    """Retorna eventos según rango de fechas"""
    start = request.GET.get('start')
    end = request.GET.get('end')

    eventos = Calendario.objects.filter(
        fecha_inicio__lte=end,
        fecha_fin__gte=start
    )

    data = [{
        'title': e.titulo,
        'start': e.fecha_inicio.isoformat(),
        'end': e.fecha_fin.isoformat(),
        'description': e.descripcion,
        'className': 'event' if e.tipo_evento != 'feriado' else 'holiday'
    } for e in eventos]

    return JsonResponse(data, safe=False)



@login_required
@csrf_exempt
def agregar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titulo = data.get('titulo')
        tipo = data.get('tipo_evento')
        inicio = data.get('inicio')
        fin = data.get('fin')
        descripcion = data.get('descripcion')
        usuario = request.user

        evento = Calendario.objects.create(
            titulo=titulo,
            tipo_evento=tipo,
            fecha_inicio=inicio,
            fecha_fin=fin,
            descripcion=descripcion,
            creado_por=usuario
        )
        return JsonResponse({'status': 'success', 'evento_id': evento.id})
    return JsonResponse({'status': 'error'})



@login_required
def funcionarios_list(request):
    funcionarios = Usuario.objects.all()
    total_funcionarios = funcionarios.count()
    funcionarios_activos = funcionarios.filter(estado='activo').count()
    licencias_activas = funcionarios.filter(estado='licencia').count()
    vacaciones_pendientes = funcionarios.filter(estado='vacaciones').count()

    context = {
        'funcionarios': funcionarios,
        'total_funcionarios': total_funcionarios,
        'funcionarios_activos': funcionarios_activos,
        'licencias_activas': licencias_activas,
        'vacaciones_pendientes': vacaciones_pendientes,
    }
    return render(request, 'cesfam/funcionarios_list.html', context)



@login_required
def solicitud_permiso_list(request):
    """
    Vista para listar las solicitudes de permiso y permitir crear nuevas.
    """
    # Crear nueva solicitud
    if request.method == 'POST' and 'solicitud_id' not in request.POST:
        form = SolicitudPermisoForm(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.fecha_solicitud = timezone.now()
            solicitud.estado = 'Pendiente'
            solicitud.save()
            return redirect('solicitud_permiso_list')
    else:
        form = SolicitudPermisoForm()

    permisos = SolicitudPermiso.objects.all().order_by('-fecha_solicitud')

    # Estadísticas rápidas
    dias_admin = 6
    dias_vacaciones = 15
    pendientes = permisos.filter(estado__iexact='Pendiente').count()
    aprobadas = permisos.filter(estado__iexact='Aprobado').count()

    context = {
        'form': form,
        'permisos': permisos,
        'dias_admin': dias_admin,
        'dias_vacaciones': dias_vacaciones,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
    }

    return render(request, 'cesfam/solicitud_permiso_list.html', context)


@login_required
def cancelar_solicitud(request, id):
    """
    Cancela una solicitud, dejando el registro en la BD como 'Cancelado'.
    """
    solicitud = get_object_or_404(SolicitudPermiso, id=id)
    if solicitud.estado == "Pendiente":
        solicitud.estado = "Cancelado"
        solicitud.save()
    return redirect('solicitud_permiso_list')


@login_required
def editar_solicitud(request, id):
    """
    Editar una solicitud Pendiente.
    """
    solicitud = get_object_or_404(SolicitudPermiso, id=id)

    if solicitud.estado != "Pendiente":
        return redirect('solicitud_permiso_list')

    # Si es POST, actualizar solicitud
    if request.method == 'POST':
        form = SolicitudPermisoForm(request.POST, request.FILES, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('solicitud_permiso_list')

    # Si se pide JSON (para cargar el modal con JS)
    if request.GET.get('json') == '1':
        data = {
            'tipo_permiso': solicitud.tipo_permiso,
            'fecha_inicio': solicitud.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': solicitud.fecha_fin.strftime('%Y-%m-%d'),
        }
        return JsonResponse(data)

    return redirect('solicitud_permiso_list')




@login_required
def licencia_list(request):
    """Vista para listar licencias médicas"""
    licencias = LicenciaMedica.objects.all()
    return render(request, 'cesfam/licencia_list.html', {'licencias': licencias})


