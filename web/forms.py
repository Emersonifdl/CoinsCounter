from django import forms

from .models import Local


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Nome de Usuário', max_length=150,
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': 'Usuário',
        }
        )
    )
    password = forms.CharField(
        label='Senha', max_length=50,
        widget=forms.PasswordInput(attrs={
            'required': True,
            'placeholder': 'Senha',
        }
        )
    )


class CadastrarLocalForm(forms.Form):
    descricao = forms.CharField(
        label='Descrição', max_length=100
    )


class CadastrarCofreForm(forms.Form):

    nome = forms.CharField(
        label='Nome', max_length=100
    )
    local = forms.ModelChoiceField(
        queryset=Local.objects.all().order_by('descricao')
    )
