"""
Para cada página que você for criar do seu site você vai construir 3 coisas:
    - url (link onde a página vai aparecer)
    - view (diz o que vai acontecer quando o usuário acessar determinado link (será puxado algo do banco de dados, será feita uma conta, ele será redirecionado, etc.))
    - template (a parte visual do que será exibido (html))
"""

"""
Explicando o request: quando você digita no navegador o endereço de um site e aperta enter, você está enviando uma requisição.
Essa requisição pode ser do tipo GET ou do tipo POST.
    GET: quando entra em um site, você está fazendo um GET naquele site, está requisitando as informações do link do site pra exibir no seu navegador.
    POST: quando você preenche um formulário e clica em enviar, está requisitando o envio de informações para o site
"""

# Create your views here.
from django.shortcuts import redirect  # para redirecionar o usuário
from django.contrib.auth.mixins import LoginRequiredMixin  # usado para exigir que o usuário esteja logado para acessar as classes/páginas em que 'LoginRequiredMixin' é passado como primeiro parâmetro
from .forms_personalizados import CriarContaForm
from django.shortcuts import reverse  # para retornar o texto do link
from .forms_personalizados import FormHomepage
from .models import Usuario


# Duas formas de construir um arquivo de views no django:
#     Function-Based Views (FBV) - você tem que criar todos os processos
#     Class-Based Views (CBV) - já trará muita coisa pronta para você


####################################################################################################
# from django.shortcuts import render
# from datetime import date

# Function-Based Views (FBV)
# def homepage(request):
#     ano_atual = {}
#     ano = date.today().year  # 'ano' recebe ano da data de hoje
#     ano_atual['ano'] = ano  # chave 'ano' recebe como valor, a variável 'ano'
#     return render(request, "homepage.html", ano_atual)  # retorna o request e a página 'homepage.html'
####################################################################################################


# TRANSFORMANDO a função homepage() em classe
from django.views.generic import TemplateView  # exibe template
from django.views.generic import FormView


# Class-Based Views (CBV)
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # se o usuário está autenticado
            # redireciona para a homefilmes
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)  # redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get("email")  # pega o texto do email que o usuário insere
        usuarios = Usuario.objects.filter(email=email)  # usuarios recebe o usuário onde o texto da coluna email é igual ao que o usuário acabou de inserir
        if usuarios:  # se existe esse usuário
            return reverse('filme:login')  # vai retornar o texto do link 'filme:login', o link correspondente ao filme login
        else:
            return reverse('filme:criarconta')

####################################################################################################
# from django.shortcuts import render
# from .models import Filme

# 'context' é um dicionário python que você vai passar dentro da sua view como parâmetro para sua página html, isso permite que ao chegar na sua página html, possa usar tags em python para carregar as informações desse dicionário

# Function-Based Views (FBV)
# url - view - html
# def homefilmes(request):
#     context = {}  # dicionário python
#     lista_filmes = Filme.objects.all()  # lista_filmes recebe todos os objetos dentro da tabela Filme
#     context['lista_filmes'] = lista_filmes  # se já existe a chave 'lista_filmes' no dicionário 'context', a chave será substituída, se não existe, será criada'
#     return render(request, "homefilmes.html", context)
####################################################################################################


# TRANSFORMANDO a função homefilmes() em classe
from .models import Filme
from django.views.generic import ListView  # ListView espera que você passe duas informações, o nome do template e o model (o modelo do banco de dados onde tem que pegar a lista (a tabela 'Filme'))


# Class-Based Views (CBV)
class Homefilmes(LoginRequiredMixin, ListView):  # LoginRequiredMixin - Exige login para acessar
    template_name = "homefilmes.html"
    model = Filme  # model recebe a tabela 'Filme'
    # A função passará para 'homefilmes.html' uma lista nomeada "object_list" com o conteúdo da tabela 'Filmes'. 'object_list' é um nome padrão
    # object_list -> lista de itens do modelo


from django.views.generic import DetailView  # para exibir os detalhes de um item


class Detalhesfilme(LoginRequiredMixin, DetailView):  # LoginRequiredMixin - Exige login para acessar
    template_name = "detalhesfilme.html"
    model = Filme
    # variável object -> 1 item do modelo

    def get(self, request, *args, **kwargs):  # redireciona o usuário para a url final
        # descobrir qual filme ele tá acessando
        filme = self.get_object()
        # somar 1 nas visualizações daquele filme
        filme.visualizacoes = filme.visualizacoes + 1
        # salvar
        filme.save()  # salvar a informação no banco de dados

        usuario = request.user
        usuario.filmes_vistos.add(filme)  # essa linha adiciona o usuário atual (id) e o filme acessado no momento (id) em filmes_vistos, no banco de dados

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):  # para não sobreescrever a função que já existe dentro do DetailView, na primeira linha de código da função que estamos criando, escreva a primeira linha assim: "context = super(Detalhesfilme, self).get_context_data(**kwargs)"
        context = super(Detalhesfilme, self).get_context_data(**kwargs)  # essa linha garante que a função que estamos criando não vai sobreescrever a função padrão do DetailView
        # Filtrar a minha tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da página, ou seja, do object
        # self.get_object()
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]  # vai retornar uma lista com 5 filmes relacionados
        context["filmes_relacionados"] = filmes_relacionados
        return context  # a lista fica disponível para usar em detalhesfilme.html


class Pesquisafilme(LoginRequiredMixin, ListView):  # LoginRequiredMixin - Exige login para acessar
    template_name = "pesquisa.html"
    model = Filme  # recebe a tabela filme

    # object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')  # pega o texto que foi digitado dentro da barra de pesquisa e passa pra variável 'termo_pesquisa'
        if termo_pesquisa:  # se existe algum texto dentro da barra de pesquisa
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa) # filtra a tabela Filme por título everifica se o termo de pesquisa está contido no título dos filmes
            return object_list
        else:
            return None


# LOGIN E LOGOUT não precisam de views aqui porque o Django já tem views padrão para login e logout

from django.views.generic import UpdateView  # a partir da tabela que você passa para ele, ele carrega os campos dessa tabela no formulário para edição
from django.contrib.auth.mixins import UserPassesTestMixin  # para solução do Álvaro


class Paginaperfil(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # LoginRequiredMixin - Exige login para acessar
    template_name = "editarperfil.html"
    model = Usuario  # tabela Usuário do banco
    fields = ['first_name', 'last_name', 'email']  # campos que permitiremos editar

    # solução do Álvaro para evitar que um usuário possa modificar o perfil de outro passando o id na barra de endereço
    def test_func(self):
        usuario = self.get_object()
        return self.request.user == usuario

    def get_success_url(self):
        return reverse('filme:homefilmes')  # vai retornar o texto do link 'filme:homefilmes', o link correspondente ao filme homefilmes


from django.views.generic import FormView  # view que por padrão passa uma variável form para nosso html


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    # como o formulário está criando um item no banco de dados
    def form_valid(self, form):  # função que verifica se todos os campos foram preenchidos corretamente
        form.save()  # salva o formulário no banco de dados
        return super().form_valid(form)

    # essa função é obrigatória
    def get_success_url(self):  # diz o que acontecerá se o formulário for bem sucedido
        return reverse('filme:login')  # vai retornar o texto do link 'filme:login', o link correspondente ao filme login
