"""
Admin do app accounts (SPEC seção 11).
Registra o modelo Perfil para facilitar a avaliação.
"""

from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'matricula', 'data_criacao')
    search_fields = ('usuario__username', 'curso', 'matricula')
