"""
URLs do app eventos (SPEC seção 7.3).

name='lista_eventos'      → /
name='detalhe_evento'     → /eventos/<int:pk>/
name='criar_evento'       → /eventos/criar/
name='editar_evento'      → /eventos/<int:pk>/editar/
name='excluir_evento'     → /eventos/<int:pk>/excluir/
name='inscrever'          → /eventos/<int:pk>/inscrever/
name='cancelar_inscricao' → /eventos/<int:pk>/cancelar/
name='meus_eventos'       → /eventos/meus/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.lista_eventos,      name='lista_eventos'),
    path('eventos/criar/',                views.criar_evento,       name='criar_evento'),
    path('eventos/meus/',                 views.meus_eventos,       name='meus_eventos'),
    path('eventos/<int:pk>/',             views.detalhe_evento,     name='detalhe_evento'),
    path('eventos/<int:pk>/editar/',      views.editar_evento,      name='editar_evento'),
    path('eventos/<int:pk>/excluir/',     views.excluir_evento,     name='excluir_evento'),
    path('eventos/<int:pk>/inscrever/',   views.inscrever,          name='inscrever'),
    path('eventos/<int:pk>/cancelar/',    views.cancelar_inscricao, name='cancelar_inscricao'),
]
