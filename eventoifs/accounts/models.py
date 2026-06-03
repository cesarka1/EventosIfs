"""
Modelos do app accounts (SPEC seção 4.1).

Perfil estende o User padrão do Django via OneToOneField.
O perfil é criado automaticamente via signal post_save no model User.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    """
    Perfil complementar do usuário.
    Criado automaticamente quando um User é salvo pela primeira vez.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuário',
    )
    curso = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Curso',
    )
    matricula = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Matrícula',
        help_text='Somente números.',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Biografia',
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de criação',
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


# ----------------------------------------------------------------
# Signal: cria/atualiza o Perfil sempre que um User for salvo
# ----------------------------------------------------------------
@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil(sender, instance, created, **kwargs):
    """Garante que todo User tenha exatamente um Perfil associado."""
    if created:
        Perfil.objects.create(usuario=instance)
    else:
        # Caso o perfil já exista, apenas salva (sem criar duplicata)
        instance.perfil.save()
