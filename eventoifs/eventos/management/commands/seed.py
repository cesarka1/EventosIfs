"""
Management command: seed
Popula o banco com dados de exemplo conforme SPEC secao 10.2.

Uso:
    python manage.py seed

Cria:
    - 1 superusuario: admin / admin1234
    - 2 alunos: aluno1, aluno2 / senha1234
    - 1 organizador: organizador1 / senha1234
    - 3 categorias: Extensao, Pesquisa, Cultura
    - 4 eventos variados (tipos e status diferentes)
    - 3 inscricoes de exemplo
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from eventos.models import Categoria, Evento, Inscricao


class Command(BaseCommand):
    help = 'Popula o banco com dados de exemplo para demonstracao e avaliacao.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Iniciando seed do banco de dados...'))

        # --------------------------------------------------------
        # Superusuario (admin)
        # --------------------------------------------------------
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.set_password('admin1234')
            admin.is_staff = True
            admin.is_superuser = True
            admin.first_name = 'Administrador'
            admin.email = 'admin@eventoifs.edu.br'
            admin.save()
            self.stdout.write(self.style.SUCCESS('  [OK] Superusuario admin criado (senha: admin1234)'))
        else:
            self.stdout.write('  [--] admin ja existe, pulando.')

        # --------------------------------------------------------
        # Usuarios comuns -- aluno1, aluno2
        # --------------------------------------------------------
        for username, first_name, email in [
            ('aluno1', 'Joao',  'joao@ifs.edu.br'),
            ('aluno2', 'Maria', 'maria@ifs.edu.br'),
        ]:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('senha1234')
                user.first_name = first_name
                user.email = email
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  [OK] Aluno {username} criado (senha: senha1234)'))
            else:
                self.stdout.write(f'  [--] {username} ja existe, pulando.')

        # --------------------------------------------------------
        # Organizador
        # --------------------------------------------------------
        org, created = User.objects.get_or_create(username='organizador1')
        if created:
            org.set_password('senha1234')
            org.first_name = 'Carlos'
            org.last_name = 'Organizador'
            org.email = 'organizador@ifs.edu.br'
            org.save()
            self.stdout.write(self.style.SUCCESS('  [OK] Organizador organizador1 criado (senha: senha1234)'))
        else:
            self.stdout.write('  [--] organizador1 ja existe, pulando.')

        # --------------------------------------------------------
        # Categorias
        # --------------------------------------------------------
        categorias = {}
        for nome, slug in [
            ('Extensao', 'extensao'),
            ('Pesquisa', 'pesquisa'),
            ('Cultura',  'cultura'),
        ]:
            cat, created = Categoria.objects.get_or_create(slug=slug, defaults={'nome': nome})
            categorias[slug] = cat
            status_msg = 'criada' if created else 'ja existe'
            self.stdout.write(f'  [--] Categoria "{nome}" {status_msg}.')

        # --------------------------------------------------------
        # Eventos (4 variados)
        # --------------------------------------------------------
        agora = timezone.now()

        eventos_dados = [
            {
                'titulo':      'Palestra: Inteligencia Artificial no IFS',
                'descricao':   'Uma introducao aos conceitos de IA e suas aplicacoes praticas no cotidiano academico.',
                'local':       'Auditorio Central - Bloco A',
                'data_inicio': agora + timedelta(days=7),
                'data_fim':    agora + timedelta(days=7, hours=3),
                'vagas':       80,
                'tipo':        Evento.TIPO_PALESTRA,
                'status':      Evento.STATUS_ABERTO,
                'cats':        ['extensao', 'pesquisa'],
            },
            {
                'titulo':      'Workshop de Desenvolvimento Web com Django',
                'descricao':   'Aprenda a construir aplicacoes web completas com Python e Django do zero ao deploy.',
                'local':       'Laboratorio de Informatica - Sala 205',
                'data_inicio': agora + timedelta(days=14),
                'data_fim':    agora + timedelta(days=14, hours=6),
                'vagas':       30,
                'tipo':        Evento.TIPO_WORKSHOP,
                'status':      Evento.STATUS_ABERTO,
                'cats':        ['extensao'],
            },
            {
                'titulo':      'Minicurso de Fotografia e Expressao Cultural',
                'descricao':   'Explore a fotografia como forma de expressao artistica e documente a cultura sergipana.',
                'local':       'Sala de Arte - Bloco C',
                'data_inicio': agora - timedelta(days=5),
                'data_fim':    agora - timedelta(days=5) + timedelta(hours=4),
                'vagas':       20,
                'tipo':        Evento.TIPO_MINICURSO,
                'status':      Evento.STATUS_ENCERRADO,
                'cats':        ['cultura'],
            },
            {
                'titulo':      'Seminario de Pesquisa Cientifica',
                'descricao':   'Apresentacao dos trabalhos de iniciacao cientifica dos alunos do IFS Campus Lagarto.',
                'local':       'Auditorio Central - Bloco A',
                'data_inicio': agora - timedelta(days=30),
                'data_fim':    agora - timedelta(days=29),
                'vagas':       100,
                'tipo':        Evento.TIPO_SEMINARIO,
                'status':      Evento.STATUS_CANCELADO,
                'cats':        ['pesquisa'],
            },
        ]

        eventos_criados = []
        for dados in eventos_dados:
            cats = dados.pop('cats')
            evento, created = Evento.objects.get_or_create(
                titulo=dados['titulo'],
                defaults={**dados, 'organizador': org},
            )
            if created:
                evento.categorias.set([categorias[c] for c in cats])
                self.stdout.write(self.style.SUCCESS(f'  [OK] Evento criado: "{evento.titulo}"'))
            else:
                self.stdout.write(f'  [--] Evento "{evento.titulo}" ja existe, pulando.')
            eventos_criados.append(evento)

        # --------------------------------------------------------
        # Inscricoes (3 de exemplo)
        # --------------------------------------------------------
        aluno1 = User.objects.get(username='aluno1')
        aluno2 = User.objects.get(username='aluno2')

        inscricoes_dados = [
            (aluno1, eventos_criados[0]),
            (aluno1, eventos_criados[1]),
            (aluno2, eventos_criados[0]),
        ]

        for participante, evento in inscricoes_dados:
            insc, created = Inscricao.objects.get_or_create(
                participante=participante,
                evento=evento,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK] Inscricao: {participante.username} -> {evento.titulo}')
                )
            else:
                self.stdout.write(f'  [--] Inscricao {participante.username}/{evento.titulo} ja existe.')

        self.stdout.write(self.style.SUCCESS('\nSeed concluido com sucesso!'))
        self.stdout.write('\nCredenciais de acesso:')
        self.stdout.write('  admin        / admin1234')
        self.stdout.write('  organizador1 / senha1234')
        self.stdout.write('  aluno1       / senha1234')
        self.stdout.write('  aluno2       / senha1234')
