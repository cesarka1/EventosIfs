"""
Modelos do app eventos (SPEC seções 4.2, 4.3, 4.4).

Categoria  — categorias de evento (slug único)
Evento     — entidade principal com 9 campos relevantes (RF03)
Inscricao  — relacionamento M:N entre User e Evento (RF05)
"""

from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    """Categoria temática de evento (ex: Extensão, Pesquisa, Cultura)."""
    nome = models.CharField(max_length=80, unique=True, verbose_name='Nome')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Evento(models.Model):
    """
    Entidade principal do domínio.
    Contém 9 campos relevantes conforme exigido pelo RF03.
    """

    # ---- Choices -------------------------------------------------------
    TIPO_PALESTRA  = 'PALESTRA'
    TIPO_WORKSHOP  = 'WORKSHOP'
    TIPO_MINICURSO = 'MINICURSO'
    TIPO_SEMINARIO = 'SEMINARIO'
    TIPO_OUTRO     = 'OUTRO'
    TIPO_CHOICES = [
        (TIPO_PALESTRA,  'Palestra'),
        (TIPO_WORKSHOP,  'Workshop'),
        (TIPO_MINICURSO, 'Minicurso'),
        (TIPO_SEMINARIO, 'Seminário'),
        (TIPO_OUTRO,     'Outro'),
    ]

    STATUS_ABERTO    = 'ABERTO'
    STATUS_ENCERRADO = 'ENCERRADO'
    STATUS_CANCELADO = 'CANCELADO'
    STATUS_CHOICES = [
        (STATUS_ABERTO,    'Aberto'),
        (STATUS_ENCERRADO, 'Encerrado'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    # ---- Campos (9 relevantes) -----------------------------------------
    titulo      = models.CharField(max_length=200, verbose_name='Título')
    descricao   = models.TextField(verbose_name='Descrição')
    local       = models.CharField(max_length=200, verbose_name='Local')
    data_inicio = models.DateTimeField(verbose_name='Data de início')
    data_fim    = models.DateTimeField(verbose_name='Data de fim')
    vagas       = models.PositiveIntegerField(verbose_name='Vagas')
    tipo        = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        default=TIPO_PALESTRA,
        verbose_name='Tipo',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ABERTO,
        verbose_name='Status',
    )
    categorias  = models.ManyToManyField(
        Categoria,
        blank=True,
        verbose_name='Categorias',
    )
    organizador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='eventos_organizados',
        verbose_name='Organizador',
    )
    criado_em   = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.titulo

    # ---- Métodos de negócio --------------------------------------------
    def vagas_disponiveis(self):
        """Retorna o número de vagas ainda disponíveis para inscrição."""
        return self.vagas - self.inscricoes.count()

    def esta_lotado(self):
        """Retorna True se não houver mais vagas disponíveis."""
        return self.vagas_disponiveis() <= 0


class Inscricao(models.Model):
    """
    Registro de inscrição de um participante em um evento (RF05).
    unique_together impede inscrições duplicadas.
    """
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name='Evento',
    )
    participante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        verbose_name='Participante',
    )
    data_inscricao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de inscrição',
    )

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ('evento', 'participante')  # impede duplicatas
        ordering = ['-data_inscricao']

    def __str__(self):
        return f'{self.participante.username} → {self.evento.titulo}'
