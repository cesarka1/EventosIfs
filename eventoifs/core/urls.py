"""
URLs raiz do projeto EventoIFS (core/urls.py).
Inclui os apps accounts e eventos conforme SPEC seção 7.1.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('eventos.urls')),
]
