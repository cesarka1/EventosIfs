"""
Views do app accounts (SPEC seção 6.1).

cadastro      → GET/POST — pública
login_view    → GET/POST — pública
logout_view   → POST     — autenticado
perfil        → GET/POST — @login_required
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import FormCadastro, FormPerfil


def cadastro(request):
    """
    Cadastra um novo usuário.
    Em caso de sucesso redireciona para login com mensagem de sucesso.
    """
    if request.method == 'POST':
        form = FormCadastro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = FormCadastro()

    return render(request, 'accounts/cadastro.html', {'form': form})


def login_view(request):
    """
    Autentica o usuário usando authenticate() e login() do Django.
    Redireciona para lista de eventos após login bem-sucedido.
    """
    if request.user.is_authenticated:
        return redirect('lista_eventos')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            # Respeita parâmetro ?next= para @login_required
            next_url = request.GET.get('next', 'lista_eventos')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Encerra a sessão e redireciona para login (aceita GET e POST)."""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


@login_required
def perfil(request):
    """
    Exibe e permite editar os dados do perfil.
    Também lista todas as inscrições do usuário autenticado.
    """
    perfil_usuario = request.user.perfil

    if request.method == 'POST':
        form = FormPerfil(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = FormPerfil(instance=perfil_usuario)

    inscricoes = request.user.inscricoes.select_related('evento').order_by('-data_inscricao')

    return render(request, 'accounts/perfil.html', {
        'form': form,
        'inscricoes': inscricoes,
    })
