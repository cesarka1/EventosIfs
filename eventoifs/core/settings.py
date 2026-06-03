"""
Configurações do projeto EventoIFS.
Gerado a partir da SPEC_eventos_academicos.md — IFS Campus Lagarto.
"""

from pathlib import Path

# ------------------------------------------------------------
# Caminhos base
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# Segurança
# ------------------------------------------------------------
SECRET_KEY = 'django-insecure-eventoifs-chave-local-substitua-em-producao'
DEBUG = True
ALLOWED_HOSTS = ['*']

# ------------------------------------------------------------
# Apps instalados
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps do projeto
    'accounts',
    'eventos',
]

# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ------------------------------------------------------------
# Templates — inclui pasta global /templates/
# ------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # base.html global aqui
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'core.wsgi.application'

# ------------------------------------------------------------
# Banco de dados — SQLite padrão
# ------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------
# Validação de senhas
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------
# Internacionalização
# ------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Maceio'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------
# Arquivos estáticos
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ------------------------------------------------------------
# Autenticação — redirecionamentos
# ------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'lista_eventos'
LOGOUT_REDIRECT_URL = 'login'

# ------------------------------------------------------------
# Armazenamento de mensagens via sessão
# ------------------------------------------------------------
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ------------------------------------------------------------
# Chave padrão para novos modelos
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
