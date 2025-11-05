from pathlib import Path

# --- BASE CONFIGURACIÓN ---
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

# --- APLICACIONES INSTALADAS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cesfam',  # Tu app principal
]

# --- MODELO DE USUARIO PERSONALIZADO ---
AUTH_USER_MODEL = 'cesfam.Usuario'

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'centrodesalud.urls'

# --- CONFIGURACIÓN DE TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # No toques esto, lo dejamos vacío
        'APP_DIRS': True,  # Django buscará dentro de cada app automáticamente
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'centrodesalud.wsgi.application'

# --- BASE DE DATOS (XAMPP / MySQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cesfam_db',  # nombre de tu base de datos
        'USER': 'root',
        'PASSWORD': '',        # vacío si usas XAMPP
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# --- VALIDADORES DE CONTRASEÑA ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- CONFIGURACIÓN LOCAL ---
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS Y MEDIA ---
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURACIÓN DE LOGIN ---
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'


#No hay sesión guardada si el navegador se cierra
SESSION_COOKIE_AGE = 3600  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
#Si hay actividad no se cierra sesion,si no hay,espera 1 hora y luego se cierra

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
