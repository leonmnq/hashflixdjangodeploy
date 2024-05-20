from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filme'

    # configuração para criar superuser automaticamente
    def ready(self):  # essa função só roda depois que o app filme estiver completamente carregado
        from .models import Usuario
        import os

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")

        usuarios = Usuario.objects.filter(email=email)  # busca na tabela Usuario no campo email, o email: "EMAIL_ADMIN"
        if not usuarios:  # se não encontrou esse email
            # cria um superuser
            Usuario.objects.create_superuser(
                username="admin",
                email=email,
                password=senha,
                is_active=True,
                is_staff=True
            )
