from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from cesfam import views as cesfam_views

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Redirección principal → Login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='cesfam/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # Página principal (solo accesible tras login)
    path('home/', cesfam_views.home, name='home'),

    # Rutas de la aplicación CESFAM
    path('', include('cesfam.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
