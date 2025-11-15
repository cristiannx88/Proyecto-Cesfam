from django.contrib.auth.decorators import login_required
from .models import Documento, Comunicado, Usuario, LicenciaMedica, SolicitudPermiso, Calendario
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ComunicadoForm, DocumentoForm, RegistroForm, SolicitudPermisoForm, LicenciaMedicaForm
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
            comunicado.id_autor = request.user
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
    year = timezone.now().year
    eventos = Calendario.objects.all().order_by('fecha_inicio')[:50]
    return render(request, 'cesfam/calendario.html', {'year': year, 'eventos': eventos})


@login_required
def eventos_json(request):
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
    """Vista para listar y crear solicitudes de permiso"""

    # Crear nueva solicitud
    if request.method == 'POST' and request.POST.get('solicitud_id') == '':
        form = SolicitudPermisoForm(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.solicitante = request.user     # ← CORREGIDO
            solicitud.fecha_solicitud = timezone.now()
            solicitud.estado = 'Pendiente'
            solicitud.save()
            return redirect('solicitud_permiso_list')
    else:
        form = SolicitudPermisoForm()

    permisos = SolicitudPermiso.objects.filter(solicitante=request.user).order_by('-fecha_solicitud')

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
    solicitud = get_object_or_404(SolicitudPermiso, id=id)
    if solicitud.estado == "Pendiente":
        solicitud.estado = "Cancelado"
        solicitud.save()
    return redirect('solicitud_permiso_list')


@login_required
def editar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudPermiso, id=id)

    if solicitud.estado != "Pendiente":
        return redirect('solicitud_permiso_list')

    if request.method == 'POST':
        form = SolicitudPermisoForm(request.POST, request.FILES, instance=solicitud)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.solicitante = solicitud.solicitante   # ← CORREGIDO
            permiso.save()
            return redirect('solicitud_permiso_list')

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
    licencias = LicenciaMedica.objects.all().select_related('funcionario', 'cargado_por')
    today = timezone.now().date()

    activas = licencias.filter(fecha_inicio__lte=today, fecha_fin__gte=today).count()
    expiradas = licencias.filter(fecha_fin__lt=today).count()
    programadas = licencias.filter(fecha_inicio__gt=today).count()
    total_dias = sum(l.dias_reposo for l in licencias)

    if request.method == 'POST':
        form = LicenciaMedicaForm(request.POST, request.FILES)
        if form.is_valid():
            licencia = form.save(commit=False)
            licencia.dias_reposo = (licencia.fecha_fin - licencia.fecha_inicio).days + 1
            licencia.numero_folio = f"LIC-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            licencia.cargado_por = request.user
            licencia.save()
            return redirect('licencia_list')
    else:
        form = LicenciaMedicaForm()

    usuarios = Usuario.objects.all()

    context = {
        'licencias': licencias,
        'form': form,
        'usuarios': usuarios,
        'activas': activas,
        'expiradas': expiradas,
        'programadas': programadas,
        'total_dias': total_dias,
        'today': today,
    }
    return render(request, 'cesfam/licencia_list.html', context)





















from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.conf import settings
import os

def descargar_comprobante(request):
    buffer = io.BytesIO()
    custom_width = 612
    custom_height = 1200  # mayor alto para todo el contenido
    c = canvas.Canvas(buffer, pagesize=(custom_width, custom_height))

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'icons', 'logo_municipio.png')
    c.setFillColor(colors.white)
    c.rect(48, custom_height - 122, 94, 54, fill=1, stroke=0)  # fondo blanco para logo
    c.drawImage(logo_path, 50, custom_height - 120, width=90, height=50, preserveAspectRatio=True, mask='auto')

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(custom_width / 2, custom_height - 115, "SOLICITA DERECHO QUE INDICA")

    y = custom_height - 150
    line_height = 20
    label_x = 60
    line_x = 170

    c.setFont("Helvetica", 11)
    fields = [
        ("NOMBRE:", 350),
        ("RUT:", 100),
        ("CARGO:", 350),
        ("TIPO DE CONTRATO:", 150),
        ("DEPARTAMENTO:", 450),
        ("LUGAR DE TRABAJO:", 450),
    ]

    for i, (label, line_len) in enumerate(fields):
        ypos = y - i * (line_height + 12)
        c.drawString(label_x, ypos, label)
        c.line(line_x, ypos - 4, line_x + line_len, ypos - 4)

    y -= 8 * (line_height + 12)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(label_x, y, "SOLICITA SE LE CONCEDA")
    c.setFont("Helvetica", 11)

    permisos = [
        "FERIADO LEGAL:",
        "PERMISO CON GOCE DE REMUNERACIONES:",
        "PERMISO SIN GOCE DE REMUNERACIONES:",
        "DEVOLUCIÓN DE TIEMPO LIBRE:",
        "OTROS PERMISOS (ESPECIFICAR):",
    ]

    for i, texto in enumerate(permisos):
        ypos = y - (i + 1) * (line_height + 7)
        c.drawString(label_x + 10, ypos, texto)
        c.line(label_x + 220, ypos - 4, label_x + 550, ypos - 4)

    y = ypos - (line_height + 30)
    c.drawString(label_x, y, "POR:")
    c.line(label_x + 40, y - 4, label_x + 80, y - 4)
    c.drawString(label_x + 90, y, "DÍAS")
    c.drawString(label_x + 140, y, "DESDE:")
    c.line(label_x + 190, y - 4, label_x + 235, y - 4)
    c.line(label_x + 238, y - 4, label_x + 285, y - 4)
    c.line(label_x + 288, y - 4, label_x + 330, y - 4)
    c.drawString(label_x + 335, y, "HASTA:")
    c.line(label_x + 380, y - 4, label_x + 410, y - 4)
    c.line(label_x + 415, y - 4, label_x + 460, y - 4)
    c.line(label_x + 465, y - 4, label_x + 510, y - 4)

    y -= line_height + 14
    c.drawString(label_x, y, "HORAS:")
    c.line(label_x + 50, y - 4, label_x + 120, y - 4)
    c.drawString(label_x + 130, y, "DESDE:")
    c.line(label_x + 180, y - 4, label_x + 220, y - 4)
    c.drawString(label_x + 230, y, "HASTA:")
    c.line(label_x + 280, y - 4, label_x + 320, y - 4)

    y -= line_height + 30
    c.drawString(label_x, y, "DÍAS PENDIENTES:")
    c.line(label_x + 110, y - 4, label_x + 260, y - 4)

    y -= line_height + 40
    c.line(custom_width - 260, y, custom_width - 60, y)
    c.drawString(custom_width - 240, y - 15, "FIRMA DEL FUNCIONARIO")

    y -= line_height + 55
    c.line(label_x, y, label_x + 200, y)
    c.drawString(label_x + 20, y - 15, "VB° NOMBRE Y FIRMA DEL JEFE DIRECTO")

    y -= line_height + 37
    c.setFont("Helvetica-Bold", 11)
    c.drawString(label_x, y, "VB° ENCARGADO REGISTRO PERSONAL:")
    c.setFont("Helvetica", 11)
    y -= line_height + 8
    c.drawString(label_x + 10, y, "NOMBRE:")
    c.line(label_x + 80, y - 4, label_x + 250, y - 4)
    y -= line_height + 5
    c.drawString(label_x + 10, y, "CARGO:")
    c.line(label_x + 80, y - 4, label_x + 250, y - 4)
    y -= line_height + 10
    c.drawString(label_x + 10, y, "OBSERVACIONES:")
    c.line(label_x + 110, y - 4, label_x + 400, y - 4)

    y += line_height * 2.3
    c.setFont("Helvetica-Bold", 11)
    c.drawString(custom_width / 2 + 20, y, "VB° JEFE GESTIÓN ADMINISTRATIVA:")
    c.setFont("Helvetica", 11)
    y -= line_height + 8
    c.drawString(custom_width / 2 + 40, y, "NOMBRE:")
    c.line(custom_width / 2 + 120, y - 4, custom_width / 2 + 430, y - 4)

    y -= line_height + 60
    c.setFont("Helvetica-Bold", 11)
    c.drawString(label_x, y, "FECHA DE ENTREGA DEL SOLICITANTE:")
    c.line(label_x + 210, y - 4, label_x + 350, y - 4)
    y -= line_height + 10
    c.drawString(label_x, y, "FECHA DE RECEPCIÓN OFIC. PERSONAL:")
    c.line(label_x + 210, y - 4, label_x + 350, y - 4)

    c.showPage()
    c.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
