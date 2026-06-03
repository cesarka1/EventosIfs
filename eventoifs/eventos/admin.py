"""
Admin do app eventos (SPEC seção 11).
Registra Categoria, Evento e Inscricao para facilitar a avaliação.
"""

from django.contrib import admin
from .models import Categoria, Evento, Inscricao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'tipo', 'status', 'data_inicio', 'vagas', 'organizador')
    list_filter   = ('tipo', 'status', 'categorias')
    search_fields = ('titulo', 'descricao', 'local')
    date_hierarchy = 'data_inicio'
    filter_horizontal = ('categorias',)


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('participante', 'evento', 'data_inscricao')
    list_filter  = ('evento',)
