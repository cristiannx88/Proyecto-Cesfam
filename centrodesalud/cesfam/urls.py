from django.urls import path
from . import views

urlpatterns = [
    # Ruta de inicio
    path('', views.home, name='home'),
    # Otras rutas
    path('documentos/', views.documentos_list, name='documentos_list'),
    path('comunicados/', views.comunicados_list, name='comunicados_list'),
    path('calendario/', views.calendario_view, name='calendario_view'),
    path('funcionarios/', views.funcionarios_list, name='funcionarios_list'),
    path('solicitud-permisos/', views.solicitud_permiso_list, name='solicitud_permiso_list'),
    path('licencias/', views.licencia_list, name='licencia_list'),
    path('base/', views.base, name='base'),
]
