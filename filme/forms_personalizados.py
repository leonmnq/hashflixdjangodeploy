from django.contrib.auth.forms import UserCreationForm  # para criar o formulário de criação de conta
from .models import Usuario  # para importar nosso modelo de usuário personalizado
from django import forms  # para adicionar um novo campo de formulário


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)  # cria um formulário que só tem o campo de email sem o rótulo 'Email:'


class CriarContaForm(UserCreationForm):  # nossa classe 'CriarContaForm' vai ser uma subclasse da 'UserCreationForm'
    # novo campo
    email = forms.EmailField()  # por padrão o campo vem obrigatório, é necessário passar como parâmetro (required=False) para ser opcional

    class Meta:  # 'UserCreationForm' do django exige que a criação da classe 'Meta' dentro da classe que está utilizando 'UserCreationForm'
        model = Usuario  # formulário será criado com base no modelo Usuario
        fields = ('username', 'email', 'first_name', 'password1', 'password2')  # passar aqui a tupla dos campos padrão juntos do novo campo

    # Solução do Alisson Silva para o email ser único
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado em outra conta! Por favor, utilize outro endereço de e-mail.")
        return email
