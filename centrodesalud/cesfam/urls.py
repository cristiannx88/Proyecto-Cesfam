from django.urls import path
from . import views

urlpatterns = [
    path('documentos/', views.documentos_list, name='documentos_list'),
    path('comunicados/', views.comunicados_list, name='comunicados_list'),
    path('calendario/', views.calendario_view, name='calendario_view'),
    path('eventos-json/', views.eventos_json, name='eventos_json'),
    path('agregar-evento/', views.agregar_evento, name='agregar_evento'),
    path('funcionarios/', views.funcionarios_list, name='funcionarios_list'),
    path('solicitud-permisos/', views.solicitud_permiso_list, name='solicitud_permiso_list'),
    path('licencias/', views.licencia_list, name='licencia_list'),
]
