# settings.py (muito importante)
# Ele que diz onde o django vai procurar determinadas informações do projeto, ou seja,
# onde vão ficar localizadas as pastas com os arquivos .html,
# onde vão ficar localizados os aplicativos, quais são os aplicativos instalados no projeto do django,
# onde vão ter as configurações do projeto, as regras gerais que vão gerir o projeto do django

"""
Django settings for hashflix project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # caminho base, onde está localizado o nosso projeto


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-6tmcqb@&zj&n#kt2uh&3*-35v00wr2ky7nt+@yx=$b0s&cj_l8'  # chave de segurança
import os  # configuração para deploy

# CONFIGURAÇÕES PARA DEPLOY
TOKEN_CSRF = os.getenv('TOKEN_CSRF')
if TOKEN_CSRF:
    SECRET_KEY = TOKEN_CSRF
    CSRF_TRUSTED_ORIGINS = ['https://hashflixdjangodeploy.onrender.com/']  # Para evitar que tentem fazer requisições
    # por outros domínios.
else:
    SECRET_KEY = 'django-insecure-6tmcqb@&zj&n#kt2uh&3*-35v00wr2ky7nt+@yx=$b0s&cj_l8'  # chave de segurança


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # atualiza automaticamente as mudanças do código no site no navegador


# configuração para deploy
#ALLOWED_HOSTS = ['*']  # todos os hosts permitidos (quando estiver tudo pronto,
# colocar a url definitiva dentro das aspas)

ALLOWED_HOSTS = ["https://hashflixdjangodeploy.onrender.com/", "localhost", "127.0.0.1"]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'filme',
    'crispy_forms',
    'crispy_bootstrap5',
]  # PASSO 1 - adicionamos o app 'filme' (passo 1) # todos os apps instalados
# crispy_forms & crispy_bootstrap5 também devem ser listados aqui como apps instalados:
# https://pypi.org/project/crispy-bootstrap5/ ou https://github.com/django-crispy-forms/crispy-bootstrap5


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware",  # modificação para deploy

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]  # processos de meio de caminho, o token de segurança para formulários, por exemplo

ROOT_URLCONF = 'hashflix.urls'  # o arquivo que tem a base de links do site, arquivo que tem os links que vão estar
# disponíveis no site

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # dentro do diretório base do projeto vão ficar os templates principais do site
        'APP_DIRS': True,  # dentro de cada app vão ficar os templates daquele app específico
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'filme.novos_context.lista_filmes_recentes',
                'filme.novos_context.lista_filmes_em_alta',
                'filme.novos_context.filme_destaque',
            ],
        },
    },
]  # o local onde vão estar os arquivos .html


WSGI_APPLICATION = 'hashflix.wsgi.application'  # arquivo de configuração de servidor


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# COMENTAR ESSE CÓDIGO PARA FAZER A MIGRAÇÃO MANUAL AO LINK EXTERNO, DESCOMENTAR APÓS A MIGRAÇÃO
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}  # caminho e nome do nosso banco de dados local


# importações para deploy
import dj_database_url
import os  # permite mexer com as variáveis de ambiente

########################################################################################################################
''' UTILIZAR ESSE CÓDIGO PARA FAZER MANUALMENTE A MIGRAÇÃO ATRAVÉS DO COMANDO: python manage.py migrate
PARA ACESSAR O LINK EXTERNO DE CONEXÃO AO DB POSTGRESQL DO RENDER '''
'''
DATABASES = {
    "default": dj_database_url.parse(
        "cole aqui o External Database URL"
    )
}
'''
# DATABASES = {
#     "default": dj_database_url.parse(
#         "postgres://db_hashflixdjangorender_40kb_user:rG4kILzgFhvvkUYqHXiGVVPFpvPn015d@dpg-cp578mocmk4c73etshdg-a.oregon-postgres.render.com/db_hashflixdjangorender_40kb"
#     )
# }
########################################################################################################################

# COMENTAR ESSE CÓDIGO PARA FAZER A MIGRAÇÃO MANUAL AO LINK EXTERNO, DESCOMENTAR APÓS A MIGRAÇÃO
DATABASE_URL = os.getenv("DATABASE_URL")  # recebe variável de ambiente com Internal Database URL
if DATABASE_URL:  # se existe a variável de ambiente
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800)
    }  # https://pypi.org/project/dj-database-url/


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

''' ATENÇÃO: isso precisa ser feito antes de fazer a primeira migração do banco (criar/atualizar tabelas), 
antes de criar o superusuário, ou seja, antes de registrar qualquer dado no banco de dados. '''
# Aqui vamos dizer que o padrão de usuário mudará para nosso modelo personalizado
AUTH_USER_MODEL = "filme.Usuario"  # o modelo que vai gerenciar usuários agora é o modelo Usuário dentro do app filme


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]  # os validadores de senha que o django vai gerenciar normalmente


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'  # língua em que aparecerão os textos e as mensagens no nosso site # padrão = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'  # fuso horário # padrão = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'  # url dos arquivos de imagem do site (CSS, JavaScript, Imagens)

STATIC_ROOT = BASE_DIR / "staticfiles"  # modificação para deploy

STATICFILES_DIRS = [
    BASE_DIR / "static",
]  # caminho onde serão salvos os arquivos de imagem do site (CSS, JavaScript, Imagens)

MEDIA_URL = 'media/'  # url dos arquivos de imagem que for feito upload pela Adminstração do Django

MEDIA_ROOT = BASE_DIR / "media"  # esse código diz pro nosso site que qualquer imagem que for feito upload
# pela Adminstração do Django, vai ser colocada dentro da pasta 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # quais serão as chaves primárias das tabelas no banco de dados

LOGIN_REDIRECT_URL = 'filme:homefilmes'  # o link que o usuário será redirecionado quando fizer login

LOGIN_URL = 'filme:login'  # o link onde o usuário faz login

# TAMBÉM SÃO NECESSÁRIAS ESSA DUAS LINHAS A SEGUIR PARA FUNCIONAMENTO DO CRISPY:
# https://pypi.org/project/crispy-bootstrap5/
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# https://github.com/django-crispy-forms/crispy-bootstrap5
