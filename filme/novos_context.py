# Criando um gerenciador de contextos:
# vamos criar aqui todas as variáveis personalizadas que todas as páginas html vão ter acesso, além das variáveis padrões do django

from .models import Filme


def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:12]  # "-" vai ordernar em ordem decrescente de acordo com a data_criacao, traz 8 resultados
    return {"lista_filmes_recentes": lista_filmes}


def lista_filmes_em_alta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:12]
    return {"lista_filmes_em_alta": lista_filmes}


def filme_destaque(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')  # "-" vai ordernar em ordem decrescente de acordo com a data_criacao
    if lista_filmes:  # se existe algum item dentro da lista 'lista_filmes'
        filme_em_destaque = lista_filmes[0]  # filme_em_destaque recebe o primeiro resultado (índice 0 traz o primeiro resultado da lista)
    else:
        filme_em_destaque = None
    return{"filme_destaque": filme_em_destaque}

# ATENÇÃO - Os contextos adicionados aqui precisam ser colocados dentro do arquivo settings.py em:
# TEMPLATES = [
#     {
#         'OPTIONS': {
#             'context_processors': [
#                 ...AQUI...
#             ],
#         },
#     },
# ]
