
> Plataforma web para cadastro, divulgação e inscrição em eventos acadêmicos do Instituto Federal de Sergipe, inspirada na aba de eventos do SUAP.
>
> **Disciplina:** Programação Web I — IFS Campus Lagarto  


---

## Integrantes

- Kauan César Ferreira — 2024000108
- Indigo Santos Tavares — 2024002739

---

## Instruções de Execução Local

```bash
# 1. Clone o repositório
git clone https://github.com/cesarka1/EventosIfs.git
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
| RF01 | Cadastro de usuário com validação de email unico                | ✅ |
| RF02 | Login e logout com autenticação nativa do Django        | ✅ |
| RF03 | Modelo Evento com 9 campos relevantes                   | ✅ |
| RF04 | CRUD completo de eventos (criar, listar, editar, excluir) | ✅ |
| RF05 | Inscrição e cancelamento de inscrição em eventos        | ✅ |
| RF06 | Validações personalizadas: data_fim > data_inicio, vagas > 0 | ✅ |
| RF07 | Busca/filtro por texto, categoria e status via GET      | ✅ |
| RF08 | Controle de acesso: apenas o coordenador do evento edita/exclui          | ✅ |
| RF09 | Herança de templates via base.html                      | ✅ |
| RF10 | Migrations e dados de exemplo (comando `seed`)          | ✅ |

---

## Capturas de Tela



1. Página inicial — lista de eventos com filtros
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fda09ced-884d-40f2-b6b0-4fa684073bb2" />
2. Página de detalhe de um evento com botão de inscrição
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1390eb01-ceec-417b-91b1-c17478863ac2" />
3. Login
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e555e0a9-e92c-41f7-be2d-e98a0ecc269e" />

4. Forms Criar Evento(Create)
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0f17a3b3-52b9-4fa1-9936-4a73556748ee" />
5. Meus Eventos(Read)
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2e02e878-dd20-4e2e-8d7b-67b013b71974" />
6. Apagar Evento(Delete)
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5c0612a6-9b0b-460a-b04b-60233d10916e" />
   


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
