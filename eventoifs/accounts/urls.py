"""
URLs do app accounts (SPEC seção 7.2).

name='cadastro'  → /accounts/cadastro/
name='login'     → /accounts/login/
name='logout'    → /accounts/logout/
name='perfil'    → /accounts/perfil/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro,     name='cadastro'),
    path('login/',    views.login_view,   name='login'),
    path('logout/',   views.logout_view,  name='logout'),
    path('perfil/',   views.perfil,       name='perfil'),
]
