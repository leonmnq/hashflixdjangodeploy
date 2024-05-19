from django.contrib import admin
from .models import Filme  # '.' porque o arquivo models.py está na mesma pasta do arquivo admin.py # importa a classe Filme
from .models import Episodio

# criação do usuário personalizado
from .models import Usuario
from django.contrib.auth.admin import UserAdmin  # importando o usuário administrativo

# Register your models here.
admin.site.register(Filme)  # essa linha faz a tabela Filme aparecer na página de admin
admin.site.register(Episodio)


# apenas para aparecer o campo personalizado filmes_vistos na administração do site
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico", {'fields': ('filmes_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)

# ATENÇÃO: o passo a seguir precisa ser feito antes de fazer a primeira migração do banco (criar/atualizar tabelas), antes de criar superusuário, ou seja, antes de registrar qualquer dado no banco de dados
# criação do usuário personalizado
admin.site.register(Usuario, UserAdmin) # tanto o usuário que vamos criar quanto o usuário administrativo ("dono do site"), vão ser gerenciados pela classe Usuario





