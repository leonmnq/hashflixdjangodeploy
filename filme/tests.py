from django.test import TestCase

# Create your tests here.
import secrets


# PARA IMPRIMIR UM TOKEN DE SEGURANÇA COM 24 CARACTERES ALFANUMÉRICOS:
print(secrets.token_hex(24))
