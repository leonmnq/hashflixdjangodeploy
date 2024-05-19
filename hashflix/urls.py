# urls.py vai definir quais serão os links do site e a relação entre eles

"""
URL configuration for hashflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns - são os links padrão do nosso site
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('filme.urls', namespace='filme')),  # como queremos que o app filme gerencie todos os links do nosso site, vamos deixar vazio '' # namespace='filme' significa que esse path vai incluir todas as urls do app que tem o nome 'filme'
]  # PASSO 2 - adicionamos o link para o app 'filme' (passo 2)
# CONEXÃO DE LINKS DINÂMICOS (namespace='filme' -> app_name = 'filme' -> name='homefilmes')


urlpatterns = urlpatterns + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)  # link onde as imagens do site serão armazenadas

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
