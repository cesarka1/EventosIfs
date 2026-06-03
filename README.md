# EventoIFS

> Plataforma web para cadastro, divulgação e inscrição em eventos acadêmicos do Instituto Federal de Sergipe, inspirada na aba de eventos do SUAP.
>
> **Disciplina:** Programação Web I — IFS Campus Lagarto  
> **Entrega:** 3 de junho de 2026

---

## Integrantes

- **[Seu Nome Completo]** — [matrícula]
- **[Nome do Parceiro]** — [matrícula]

---

## Instruções de Execução Local

```bash
# 1. Clone o repositório
git clone <URL-DO-REPOSITORIO>
cd EventosIfs

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
# source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Entre na pasta do projeto Django
cd eventoifs

# 5. Gere e aplique as migrations
python manage.py makemigrations accounts
python manage.py makemigrations eventos
python manage.py migrate

# 6. Popule o banco com dados de exemplo
python manage.py seed

# 7. Inicie o servidor
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000/**

### Credenciais de acesso (após seed)

| Usuário       | Senha      | Perfil        |
|---------------|------------|---------------|
| admin         | admin1234  | Superusuário  |
| organizador1  | senha1234  | Organizador   |
| aluno1        | senha1234  | Aluno         |
| aluno2        | senha1234  | Aluno         |

---

## Requisitos Funcionais Implementados

| RF   | Descrição                                               | Status |
|------|---------------------------------------------------------|--------|
| RF01 | Cadastro de usuário com validação de e-mail único       | ✅ |
| RF02 | Login e logout com autenticação nativa do Django        | ✅ |
| RF03 | Modelo Evento com 9 campos relevantes                   | ✅ |
| RF04 | CRUD completo de eventos (criar, listar, editar, excluir) | ✅ |
| RF05 | Inscrição e cancelamento de inscrição em eventos        | ✅ |
| RF06 | Validações personalizadas: data_fim > data_inicio, vagas > 0 | ✅ |
| RF07 | Busca/filtro por texto, categoria e status via GET      | ✅ |
| RF08 | Controle de acesso: apenas o dono edita/exclui          | ✅ |
| RF09 | Herança de templates via base.html                      | ✅ |
| RF10 | Migrations e dados de exemplo (comando `seed`)          | ✅ |

---

## Capturas de Tela

> *(Adicione aqui capturas de tela da aplicação funcionando)*

1. Página inicial — lista de eventos com filtros
2. Página de detalhe de um evento com botão de inscrição

---

## Estrutura do Projeto

```
EventosIfs/
├── eventoifs/              ← projeto Django
│   ├── core/               ← configurações
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── accounts/           ← app de autenticação
│   │   ├── models.py       ← Perfil (OneToOne com User)
│   │   ├── views.py        ← cadastro, login, logout, perfil
│   │   ├── forms.py        ← FormCadastro, FormPerfil
│   │   ├── urls.py
│   │   └── templates/accounts/
│   │       ├── login.html
│   │       ├── cadastro.html
│   │       └── perfil.html
│   ├── eventos/            ← app principal
│   │   ├── models.py       ← Categoria, Evento, Inscricao
│   │   ├── views.py        ← CRUD + inscrição + busca
│   │   ├── forms.py        ← FormEvento, FormBusca
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── management/commands/seed.py
│   │   └── templates/eventos/
│   │       ├── lista.html
│   │       ├── detalhe.html
│   │       ├── criar.html
│   │       ├── editar.html
│   │       ├── _form_evento.html
│   │       ├── confirmar_exclusao.html
│   │       └── meus_eventos.html
│   ├── templates/
│   │   └── base.html       ← template base global
│   └── static/css/
│       └── style.css
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **Django 4.2+**
- **SQLite** — banco de dados padrão
- **Bootstrap 5** — via CDN
- **Bootstrap Icons** — via CDN
- HTML + CSS puro nos templates
