from django.contrib.auth.decorators import login_required
from .models import Documento, Comunicado, Usuario, LicenciaMedica, SolicitudPermiso
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ComunicadoForm, DocumentoForm


def home(request):
    """Vista para la página de inicio"""
    context = {
        'total_documentos': Documento.objects.count(),
        'total_funcionarios': Usuario.objects.count(),
        'total_permisos': SolicitudPermiso.objects.count(),
        'comunicados_recientes': Comunicado.objects.all()[:5]
    }
    return render(request, 'cesfam/home.html', context)



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



def calendario_view(request):
    """Vista para el calendario"""
    return render(request, 'cesfam/calendario.html')

def funcionarios_list(request):
    """Vista para listar funcionarios"""
    funcionarios = Usuario.objects.all()
    return render(request, 'cesfam/funcionarios_list.html', {'funcionarios': funcionarios})

def solicitud_permiso_list(request):
    """Vista para listar solicitudes de permiso"""
    permisos = SolicitudPermiso.objects.all()
    return render(request, 'cesfam/solicitud_permiso_list.html', {'permisos': permisos})

def licencia_list(request):
    """Vista para listar licencias médicas"""
    licencias = LicenciaMedica.objects.all()
    return render(request, 'cesfam/licencia_list.html', {'licencias': licencias})

def base(request):
    """Vista para la página base"""
    return render(request, 'cesfam/base.html')