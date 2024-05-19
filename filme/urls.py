"""
Para cada página que você for criar do seu site você vai construir 3 coisas:
    - url (link onde a página vai aparecer)
    - view (diz o que vai acontecer quando o usuário acessar determinado link (será puxado algo do banco de dados, será feita uma conta, ele será redirecionado, etc.))
    - template (a parte visual do que será exibido (html))
"""

from django.urls import path, include
from django.urls import reverse_lazy  # modo de passar o reverse dentro do urls.py

# deixaremos de usar função e usaremos classe
# from .views import homepage  # importa a função homepage do arquivo views.py ('.views' porque está na mesma pasta)

# deixaremos de usar função e usaremos classe
# from .views import homefilmes

# importando classes
from .views import Homepage  # importa a classe Homepage do arquivo views.py ('.views' porque está na mesma pasta)
from .views import Homefilmes
from .views import Detalhesfilme
from .views import Pesquisafilme
from .views import Paginaperfil
from .views import Criarconta
from django.contrib.auth import views as auth_view  # para gerenciar login/logout do usuário

app_name = 'filme'  # agora é possível acessar o link de cada página do app filme pelo name='nome da página'

# PASSO 4 - Configurar os links do app filme
urlpatterns = [
#    path('', homepage),  # quando não coloca os parênteses da função ele automaticamente passa o request como parâmetro para função
    path('', Homepage.as_view(), name='homepage'),
#    path('filmes/', homefilmes),  # quando não coloca os parênteses da função ele automaticamente passa o request como parâmetro para função
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', Detalhesfilme.as_view(), name='detalhesfilme'),  # pk = primary key = id, ou seja, vai acrescentar o id de cada filme na barra de endereço do navegador, mostrando dinamicamente, uma página de detalhe para cada filme
    path('pesquisa/', Pesquisafilme.as_view(), name='pesquisafilme'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),  # LoginView do Django já vem com formulário 'embutido', a página login.html vai receber esse form
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),  # LogoutView do Django já vem com formulário 'embutido', a página logout.html vai receber esse form
    path('editarperfil/<int:pk>', Paginaperfil.as_view(), name='editarperfil'),  # pk = primary key = id, ou seja, vai acrescentar o id de cada usuario na barra de endereço do navegador, mostrando dinamicamente, uma página de editar perfil para cada usuário
    path('criarconta/', Criarconta.as_view(), name='criarconta'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html', success_url=reverse_lazy('filme:homefilmes')), name='mudarsenha'),
]
# CONEXÃO DE LINKS DINÂMICOS (namespace='filme' -> app_name = 'filme' -> name='homefilmes')
