from django.db import models
from django.utils import timezone  # para salvar a hora de criação do filme
from django.contrib.auth.models import AbstractUser  # necessário fazer essa importação para podermos criar nosso usuário personalizado

# Create your models here.

# LISTA_CATEGORIAS = (
#     ("ANALISES", "Análises"),
#     ("PROGRAMACAO", "Programação"),
#     ("APRESENTACAO", "Apresentação"),
#     ("OUTROS", "Outros")
# )  # Ex: (armazenar_no_banco, aparecer_pro_usuario)

LISTA_CATEGORIAS = (
    ("ACAO", "Ação"),
    ("ANIMACAO", "Animação"),
    ("ANIME", "Anime"),
    ("AVENTURA", "Aventura"),
    ("CINEMADAARTE", "Cinema de arte"),
    ("CHANCHADA", "Chanchada"),
    ("COMEDIA", "Comédia"),
    ("COMEDIADEACAO", "Comédia de ação"),
    ("COMEDIADETERROR", "Comédia de terror"),
    ("COMEDIADRAMATICA", "Comédia dramática"),
    ("COMEDIAROMANTICA", "Comédia romântica"),
    ("DANCA", "Dança"),
    ("DOCUMENTARIO", "Documentário"),
    ("DOCUFICCAO", "Docuficção"),
    ("DRAMA", "Drama"),
    ("ESPIONAGEM", "Espionagem"),
    ("FAROESTE", "Faroeste"),
    ("FANTASIA", "Fantasia"),
    ("FANTASIACIENTIFICA", "Fantasia científica"),
    ("FICCAOCIENTIFICA", "Ficção científica"),
    ("FILMESCOMTRUQUES", "Filmes com truques"),
    ("FILMESDEGUERRA", "Filmes de guerra"),
    ("MISTERIO", "Mistério"),
    ("MUSICAL", "Musical"),
    ("FILMEPOLICIAL", "Filme policial"),
    ("ROMANCE", "Romance"),
    ("SUSPENSE", "Suspense"),
    ("TERROR", "Terror"),
    ("THRILLER", "Thriller"),
    ("OUTROS", "Outros")
)


# PASSO 3 - criar o filme (passo 3)
class Filme(models.Model):  # Filme é uma subclasse de models.Model
    titulo = models.CharField(max_length=100)  # CharField é campo de texto

    thumb_link = models.URLField(default='')  # minha modificação para salvar endereço online das thumbs, podendo acessar o link online

    #thumb = models.ImageField(upload_to='thumb_filmes')  # a imagem será armazenada dentro da pasta 'thumb_filmes' dentro da pasta 'media'
    descricao = models.TextField(max_length=1000)  # TextField é um bloco para texto
    categoria = models.CharField(max_length=30, choices=LISTA_CATEGORIAS)  # o usuário escolhe uma das categorias na LISTA_CATEGORIAS
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)  # '.now' sem os parênteses para registrar a hora de criação e não a hora de visualização

    # essa função padrão do python diz para cada classe do python o que vai aparecer quando um usuário der um 'print' em algum item dessa classe
    def __str__(self):  # retorna o formato string de um objeto da classe Filme
        return self.titulo  # retorna o título do filme em formato string


# ATENÇÃO: isso precisa ser feito antes de fazer a primeira migração do banco (criar/atualizar tabelas), antes de criar superusuário, ou seja, antes de registrar qualquer dado no banco de dados
# Vamos criar o usuário personalizado que vai importar o usuário padrão do django
# Vamos fazer importações e criar uma linha em admin.py
# E depois, lá no settings.py, dizer que padrão de usuário mudará para nosso modelo personalizado
class Usuario(AbstractUser):
    # acrescentar aqui apenas os campos novos, que não existem dentro do AbstractUser
    filmes_vistos = models.ManyToManyField("Filme")  # relação de muitos para muitos: ManyToManyField. Vários usuários que viram o mesmo filme e muitos filmes foram vistos por um usuário só.
    # filmes_vistos serão um item da classe Filme

# Após realizar o processo de criação do usuário personalizado, é necessário rodar os 2 comandos: 'python manage.py makemigrations' e 'python manage.py migrate'  # sempre que faz uma modificação no banco de dados, tem que fazer uma migration que é o que vai atualizar o banco de dados


# relação de um para muitos, um filme pode ter muitos episódios: utiliza foreignkey
# criar os episódios
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)     # campo da chave estrangeira (definir sempre como primeiro campo da tabela)
    # related_name permite acessar todos os episódios de um filme específico
    # on_delete=models.CASCADE significa que se for deletado um filme, serão deletados todos os episódios relacionados aquele filme em modo cascata

    titulo = models.CharField(max_length=100)
    video = models.URLField()  # link

    def __str__(self):  # retorna o formato string de um objeto da classe Episodio
        return self.filme.titulo + " - " + self.titulo  # retorna o título do filme mais o título do episódio
    # visualizar no admin do site



