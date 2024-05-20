from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'


    # configuração para criar superuser automaticamente
    # (essa função retorna uma mensagem de alerta do Render, manter comentada )
    # def ready(self):  # essa função só roda depois que o app filme estiver completamente carregado
    #     from .models import Usuario
    #     import os
    #
    #     email = os.getenv("EMAIL_ADMIN")
    #     senha = os.getenv("SENHA_ADMIN")
    #
    #     usuarios = Usuario.objects.filter(email=email)  # busca na tabela Usuario no campo email, o email: "EMAIL_ADMIN"
    #     if not usuarios:  # se não encontrou esse email
    #         # cria um superuser
    #         Usuario.objects.create_superuser(
    #             username="admin",
    #             email=email,
    #             password=senha,
    #             is_active=True,
    #             is_staff=True
    #         )


""" (O Render retornar essa mensagem durante o deploy: Aviso de tempo de execução: o acesso ao banco de dados 
durante a inicialização do aplicativo é desencorajado. Para corrigir esse aviso, evite executar consultas em 
AppConfig.ready() ou quando os módulos do seu aplicativo forem importados.) """
