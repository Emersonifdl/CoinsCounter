import hashlib
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action

from web.forms import LoginForm, CadastrarLocalForm, CadastrarCofreForm
from web.models import Cofre, Local, Transacao

from .serializers import TransacaoSerializer


class LoginRequiredView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)


class DashboardView(LoginRequiredView):

    def __init__(self):
        super(DashboardView, self).__init__()

    def get(self, request):
        cofres = Cofre.objects.all().count()
        transacoes = Transacao.objects.all().count()
        locais = Local.objects.all().count()

        context = {
            'cofres': cofres,
            'transacoes': transacoes,
            'locais': locais,
        }

        return render(request, 'web/dashboard.html', context)


class LoginView(View):

    def get(self, request):

        # Verifica se já existe algum usuário autenticado.
        if request.user.is_authenticated:
            messages.error(request, 'User is already authenticated.')
            return redirect('dashboard')

        context = {
            'form': LoginForm(),
        }

        return render(request, 'web/login.html', context)

    def post(self, request):

        form = LoginForm(request.POST)

        # Prepara a página de redirecionamento após o login.
        next_page = request.GET.get('next')
        if next_page is None:
            next_page = 'dashboard'

        if not form.is_valid():
            messages.error(request, 'Form Invalid.')
            context = {
                'form': form,
            }
            return render(request, 'web/login.html', context)

        user = form.cleaned_data['login']
        password = form.cleaned_data['password']

        user_auth = authenticate(request, username=user,
                                 password=password)
        # Se o usuário foi autenticado com sucesso, realize abra a sessão.
        if user_auth is not None:
            login(request, user_auth)
            return redirect(next_page)
        else:
            messages.error(request, 'Login and/or password incorrect.')
            context = {
                'form': form,
            }
            return render(request, 'web/login.html', context)


class LogoutView(View):

    def get(self, request):
        # Verifica se o usuário não está autenticado.
        if not request.user.is_authenticated:
            messages.error(request, 'User must be logged in')
            return redirect('dashboard')

        logout(request)
        return redirect('dashboard')


class CadastrarLocalView(LoginRequiredView):

    def __init__(self):
        super(CadastrarLocalView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request):

        """
            if not request.user.groups.filter(name='Administrator').exists():
            return HttpResponseForbidden('Não permitido')
        """
        context = {
            'form': CadastrarLocalForm(),
        }

        return render(
            request,
            'web/local/cadastrar_local.html',
            context
        )

    def post(self, request):

        form = CadastrarLocalForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']

            # Salva o Local.
            Local.objects.create(descricao=descricao)

            messages.success(request, 'Local cadastrado com sucesso.')
            return redirect('dashboard')
        else:
            return HttpResponseBadRequest('Formulário inválido.')


class ListarLocalView(LoginRequiredView):
    def __init__(self):
        super(ListarLocalView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request):
        locais = Local.objects.all()

        context = {
            'locais': locais,
        }

        return render(
            request,
            'web/local/listar_locais.html',
            context
        )


class DeletarLocalView(LoginRequiredView):
    def __init__(self):
        super(DeletarLocalView, self).__init__()

    def get(self, request, id):

        # Verifica se a despesa existe.
        try:
            local = Local.objects.get(id=id)
        except Local.DoesNotExist:
            messages.error(
                request, 'Não existe um Local com o id {}.'.format(id)
            )
            return redirect('listar_locais')

        local.delete()

        messages.success(
            request, 'Local removido com sucesso.'
        )
        return redirect('listar_locais')

class DetalharLocalView(LoginRequiredView):
    def __init__(self):
        super(DetalharLocalView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request, id):
        # Verifica se a Cofre existe.
        try:
            local = Local.objects.get(id=id)
        except Cofre.DoesNotExist:
            messages.error(
                request, 'Não existe um Local com o token {}.'.format(id)
            )
            return redirect('listar_locais')

        saldo = Cofre.objects.filter(local=local).aggregate(total=Sum('saldo'))['total']
        cofres = Cofre.objects.filter(local=local).count()

        context = {
            'local': local,
            'saldo': saldo,
            'cofres': cofres,
        }

        return render(
            request,
            'web/local/detalhes_local.html',
            context
        )


class CadastrarCofreView(LoginRequiredView):

    def __init__(self):
        super(CadastrarCofreView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request):

        context = {
            'form': CadastrarCofreForm(),
        }

        return render(
            request,
            'web/cofre/cadastrar_cofre.html',
            context
        )

    def post(self, request):

        form = CadastrarCofreForm(request.POST)
        if form.is_valid():
            token_md5 = hashlib.md5()
            token_md5.update(str(datetime.now()).encode())

            nome = form.cleaned_data['nome']
            local = form.cleaned_data['local']
            token = token_md5.hexdigest()

            # Salva o Local.
            Cofre.objects.create(
                nome=nome,
                local=local,
                saldo=0.0,
                token=token
            )

            messages.success(request, 'Cofre cadastrado com sucesso.')
            return redirect('dashboard')
        else:
            return HttpResponseBadRequest('Formulário inválido.')


class ListarCofreView(LoginRequiredView):
    def __init__(self):
        super(ListarCofreView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request):
        cofres = Cofre.objects.all()

        context = {
            'cofres': cofres,
        }

        return render(
            request,
            'web/cofre/listar_cofres.html',
            context
        )


class DetalharCofreView(LoginRequiredView):
    def __init__(self):
        super(DetalharCofreView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request, token):
        # Verifica se a Cofre existe.
        try:
            cofre = Cofre.objects.get(token=token)
        except Cofre.DoesNotExist:
            messages.error(
                request, 'Não existe um Cofre com o token {}.'.format(token)
            )
            return redirect('listar_cofres')

        transacoes = Transacao.objects.filter(cofre=cofre, lido=False)

        if transacoes:
            for transacao in transacoes:
                transacao.lido = True
                transacao.save()
                cofre.saldo += transacao.valor
            cofre.save()


        context = {
            'cofre': cofre,
        }

        return render(
            request,
            'web/cofre/detalhes_cofre.html',
            context
        )


class DeletarCofreView(LoginRequiredView):
    def __init__(self):
        super(DeletarCofreView, self).__init__()

    def get(self, request, token):

        # Verifica se a Cofre existe.
        try:
            cofre = Cofre.objects.get(token=token)
        except Cofre.DoesNotExist:
            messages.error(
                request, 'Não existe um Cofre com o token {}.'.format(token)
            )
            return redirect('listar_cofres')

        cofre.delete()

        messages.success(
            request, 'Cofre removido com sucesso.'
        )
        return redirect('listar_cofres')


class ListarTransacaoView(LoginRequiredView):
    def __init__(self):
        super(ListarTransacaoView, self).__init__()
        # self.ano = datetime.now().year

    def get(self, request):
        transacoes = Transacao.objects.all()

        context = {
            'transacoes': transacoes,
        }

        return render(
            request,
            'web/transacao/listar_transacoes.html',
            context
        )


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
