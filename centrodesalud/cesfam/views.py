from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Documento, Comunicado, Usuario, LicenciaMedica, SolicitudPermiso

def home(request):
    """Vista para la página de inicio"""
    context = {
        'total_documentos': Documento.objects.count(),
        'total_funcionarios': Usuario.objects.count(),
        'total_permisos': SolicitudPermiso.objects.count(),
        'comunicados_recientes': Comunicado.objects.all()[:5]
    }
    return render(request, 'cesfam/home.html', context)

def documentos_list(request):
    """Vista para listar documentos"""
    documentos = Documento.objects.all()
    return render(request, 'cesfam/documentos_list.html', {'documentos': documentos})

def comunicados_list(request):
    """Vista para listar comunicados"""
    comunicados = Comunicado.objects.all()
    return render(request, 'cesfam/comunicados_list.html', {'comunicados': comunicados})

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
