"""
Views do app eventos (SPEC seção 6.2).

lista_eventos      → GET          — pública (RF07 busca/filtro)
detalhe_evento     → GET          — pública
criar_evento       → GET/POST     — @login_required
editar_evento      → GET/POST     — @login_required + dono (RF08)
excluir_evento     → GET/POST     — @login_required + dono (RF08)
inscrever          → POST         — @login_required
cancelar_inscricao → POST         — @login_required
meus_eventos       → GET          — @login_required
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Evento, Inscricao
from .forms import FormEvento, FormBusca


# ----------------------------------------------------------------
# Views públicas
# ----------------------------------------------------------------

def lista_eventos(request):
    """
    Lista todos os eventos com suporte a busca e filtro via GET (RF07).
    Filtros disponíveis: texto livre (q), categoria e status.
    """
    eventos = Evento.objects.prefetch_related('categorias').select_related('organizador')
    form_busca = FormBusca(request.GET)

    if form_busca.is_valid():
        q         = form_busca.cleaned_data.get('q')
        categoria = form_busca.cleaned_data.get('categoria')
        status    = form_busca.cleaned_data.get('status')

        if q:
            # Busca por título OU descrição usando Q()
            eventos = eventos.filter(
                Q(titulo__icontains=q) | Q(descricao__icontains=q)
            )
        if categoria:
            eventos = eventos.filter(categorias=categoria)
        if status:
            eventos = eventos.filter(status=status)

    return render(request, 'eventos/lista.html', {
        'eventos': eventos,
        'form_busca': form_busca,
    })


def detalhe_evento(request, pk):
    """Exibe todos os dados de um evento, inscrições e ações disponíveis."""
    evento = get_object_or_404(Evento, pk=pk)
    ja_inscrito = False

    if request.user.is_authenticated:
        ja_inscrito = evento.inscricoes.filter(participante=request.user).exists()

    # Lista de participantes visível apenas para o organizador
    participantes = None
    if request.user.is_authenticated and evento.organizador == request.user:
        participantes = evento.inscricoes.select_related('participante').all()

    return render(request, 'eventos/detalhe.html', {
        'evento': evento,
        'ja_inscrito': ja_inscrito,
        'participantes': participantes,
    })


# ----------------------------------------------------------------
# Views protegidas — CRUD de eventos
# ----------------------------------------------------------------

@login_required
def criar_evento(request):
    """
    Cria um novo evento.
    O organizador é definido como request.user automaticamente.
    """
    if request.method == 'POST':
        form = FormEvento(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user  # não exposto no form
            evento.save()
            form.save_m2m()  # salva relacionamento M2M (categorias)
            messages.success(request, f'Evento "{evento.titulo}" criado com sucesso!')
            return redirect('detalhe_evento', pk=evento.pk)
    else:
        form = FormEvento()

    return render(request, 'eventos/criar.html', {'form': form})


@login_required
def editar_evento(request, pk):
    """
    Edita um evento existente.
    Apenas o organizador pode editar (RF08).
    """
    evento = get_object_or_404(Evento, pk=pk)

    # Verificação de dono (RF08 / seção 12)
    if evento.organizador != request.user:
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('detalhe_evento', pk=evento.pk)

    if request.method == 'POST':
        form = FormEvento(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Evento "{evento.titulo}" atualizado com sucesso!')
            return redirect('detalhe_evento', pk=evento.pk)
    else:
        form = FormEvento(instance=evento)

    return render(request, 'eventos/editar.html', {'form': form, 'evento': evento})


@login_required
def excluir_evento(request, pk):
    """
    Exclui um evento após confirmação.
    Apenas o organizador pode excluir (RF08).
    """
    evento = get_object_or_404(Evento, pk=pk)

    # Verificação de dono (RF08 / seção 12)
    if evento.organizador != request.user:
        messages.error(request, 'Você não tem permissão para excluir este evento.')
        return redirect('detalhe_evento', pk=evento.pk)

    if request.method == 'POST':
        titulo = evento.titulo
        evento.delete()
        messages.success(request, f'Evento "{titulo}" excluído com sucesso.')
        return redirect('lista_eventos')

    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})


# ----------------------------------------------------------------
# Views de inscrição
# ----------------------------------------------------------------

@login_required
def inscrever(request, pk):
    """
    Inscreve o usuário autenticado no evento.
    Verifica se o evento está ABERTO e não está lotado antes de prosseguir.
    Usa get_or_create para evitar duplicatas.
    """
    evento = get_object_or_404(Evento, pk=pk)

    if evento.status != Evento.STATUS_ABERTO:
        messages.warning(request, 'Este evento não está aberto para inscrições.')
        return redirect('detalhe_evento', pk=pk)

    if evento.esta_lotado():
        messages.warning(request, 'Este evento não possui mais vagas disponíveis.')
        return redirect('detalhe_evento', pk=pk)

    inscricao, criada = Inscricao.objects.get_or_create(
        evento=evento,
        participante=request.user,
    )

    if criada:
        messages.success(request, f'Inscrição realizada com sucesso em "{evento.titulo}"!')
    else:
        messages.info(request, 'Você já está inscrito neste evento.')

    return redirect('detalhe_evento', pk=pk)


@login_required
def cancelar_inscricao(request, pk):
    """
    Cancela a inscrição do usuário autenticado no evento.
    Deleta a inscrição se existir.
    """
    evento = get_object_or_404(Evento, pk=pk)
    deleted, _ = Inscricao.objects.filter(
        evento=evento,
        participante=request.user,
    ).delete()

    if deleted:
        messages.success(request, f'Inscrição em "{evento.titulo}" cancelada.')
    else:
        messages.warning(request, 'Você não estava inscrito neste evento.')

    return redirect('detalhe_evento', pk=pk)


@login_required
def meus_eventos(request):
    """Lista os eventos criados pelo usuário autenticado."""
    eventos = Evento.objects.filter(
        organizador=request.user
    ).prefetch_related('categorias').order_by('-criado_em')

    return render(request, 'eventos/meus_eventos.html', {'eventos': eventos})
