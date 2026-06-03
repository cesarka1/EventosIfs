# SPEC — Sistema de Eventos Acadêmicos
> Baseado no trabalho prático de Programação Web I — IFS Campus Lagarto  
> Contexto inspirado na aba de Eventos do SUAP Acadêmico  
> Framework: Django | Entrega: 3 de junho de 2026

---

## 1. VISÃO GERAL DO SISTEMA

**Nome do projeto:** EventoIFS  
**Descrição:** Plataforma web para cadastro, divulgação e inscrição em eventos acadêmicos do Instituto Federal de Sergipe, inspirada na aba de eventos do SUAP. Alunos podem se inscrever em eventos; organizadores podem criar e gerenciar os seus.

**Stack obrigatória:**
- Python 3.11+
- Django 4.2+
- SQLite (banco padrão)
- HTML + CSS puro nos templates (sem React, sem Vue)
- Bootstrap 5 via CDN (para agilidade de interface)

---

## 2. ESTRUTURA DO PROJETO

```
eventoifs/              ← pasta raiz do projeto Django
├── core/               ← configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/           ← app de autenticação e perfil
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── cadastro.html
│           └── perfil.html
├── eventos/            ← app principal do domínio
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── eventos/
│           ├── lista.html
│           ├── detalhe.html
│           ├── criar.html
│           ├── editar.html
│           └── confirmar_exclusao.html
├── templates/
│   └── base.html       ← template base global
├── static/
│   └── css/
│       └── style.css
├── fixtures/
│   └── dados_iniciais.json
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## 3. APPS E RESPONSABILIDADES

### 3.1 App `accounts`
Responsável por tudo relacionado à identidade do usuário:
- Cadastro de novo usuário
- Login e logout
- Visualização e edição do perfil

### 3.2 App `eventos`
Responsável pelo domínio principal:
- Modelo `Categoria`
- Modelo `Evento`
- Modelo `Inscricao`
- CRUD completo de eventos
- Inscrição e cancelamento de inscrição
- Busca e filtro de eventos

---

## 4. MODELOS (models.py)

### 4.1 App `accounts` — modelo `Perfil`

Estende o usuário padrão do Django via OneToOneField.

```
Perfil
├── usuario        → OneToOneField(User, on_delete=CASCADE)
├── curso          → CharField(max_length=100, blank=True)
├── matricula      → CharField(max_length=20, blank=True)
├── bio            → TextField(blank=True)
└── data_criacao   → DateTimeField(auto_now_add=True)
```

**Observações:**
- Criar o perfil automaticamente via signal `post_save` no model `User`
- O campo `matricula` deve aceitar apenas dígitos — validação personalizada no form

### 4.2 App `eventos` — modelo `Categoria`

```
Categoria
├── nome    → CharField(max_length=80, unique=True)
└── slug    → SlugField(unique=True)
```

### 4.3 App `eventos` — modelo `Evento` ← entidade principal (RF03)

Mínimo de 5 campos relevantes exigidos. Este modelo tem 9:

```
Evento
├── titulo         → CharField(max_length=200)
├── descricao      → TextField()
├── local          → CharField(max_length=200)
├── data_inicio    → DateTimeField()
├── data_fim       → DateTimeField()
├── vagas          → PositiveIntegerField()
├── tipo           → CharField(max_length=30, choices=[PALESTRA, WORKSHOP, MINICURSO, SEMINARIO, OUTRO])
├── status         → CharField(max_length=20, choices=[ABERTO, ENCERRADO, CANCELADO], default=ABERTO)
├── categorias     → ManyToManyField(Categoria)         ← RF05
├── organizador    → ForeignKey(User, on_delete=CASCADE) ← RF05
└── criado_em      → DateTimeField(auto_now_add=True)
```

**Método obrigatório no modelo:**
- `vagas_disponiveis()` → retorna `vagas - inscricoes.count()`
- `esta_lotado()` → retorna `True` se vagas_disponiveis() <= 0
- `__str__()` → retorna o título do evento

### 4.4 App `eventos` — modelo `Inscricao` (RF05)

```
Inscricao
├── evento         → ForeignKey(Evento, on_delete=CASCADE, related_name='inscricoes')
├── participante   → ForeignKey(User, on_delete=CASCADE, related_name='inscricoes')
└── data_inscricao → DateTimeField(auto_now_add=True)
```

**Constraint obrigatória:**
- `unique_together = ('evento', 'participante')` — impede inscrição duplicada

---

## 5. FORMULÁRIOS (forms.py)

### 5.1 `accounts/forms.py`

**`FormCadastro`** — herda de `UserCreationForm`
- Campos: `username`, `first_name`, `last_name`, `email`, `password1`, `password2`
- Validação personalizada: `email` deve ser único no sistema (verificar se já existe outro User com o mesmo email)

**`FormPerfil`** — herda de `ModelForm` para `Perfil`
- Campos: `curso`, `matricula`, `bio`
- Validação personalizada: `matricula` deve conter apenas números (`isdigit()`)

### 5.2 `eventos/forms.py`

**`FormEvento`** — herda de `ModelForm` para `Evento`
- Campos: `titulo`, `descricao`, `local`, `data_inicio`, `data_fim`, `vagas`, `tipo`, `status`, `categorias`
- Validação personalizada obrigatória (RF06):
  - `data_fim` deve ser posterior a `data_inicio` — lançar `ValidationError` caso contrário
  - `vagas` deve ser maior que zero

**`FormBusca`** — form simples (não ModelForm)
- Campos: `q` (texto livre), `categoria` (ModelChoiceField), `status` (ChoiceField)
- Método GET (não POST)

---

## 6. VIEWS (views.py)

### 6.1 `accounts/views.py`

| View | URL | Método | Proteção |
|---|---|---|---|
| `cadastro` | `/accounts/cadastro/` | GET/POST | pública |
| `login_view` | `/accounts/login/` | GET/POST | pública |
| `logout_view` | `/accounts/logout/` | POST | autenticado |
| `perfil` | `/accounts/perfil/` | GET/POST | @login_required |

**Comportamentos:**
- `cadastro`: salva o usuário e redireciona para login com mensagem de sucesso
- `login_view`: usa `authenticate()` e `login()` do Django; redireciona para lista de eventos
- `logout_view`: usa `logout()` do Django; redireciona para login
- `perfil`: exibe e permite editar dados do perfil + lista as inscrições do usuário

### 6.2 `eventos/views.py`

| View | URL | Método | Proteção |
|---|---|---|---|
| `lista_eventos` | `/` | GET | pública |
| `detalhe_evento` | `/eventos/<int:pk>/` | GET | pública |
| `criar_evento` | `/eventos/criar/` | GET/POST | @login_required |
| `editar_evento` | `/eventos/<int:pk>/editar/` | GET/POST | @login_required + dono |
| `excluir_evento` | `/eventos/<int:pk>/excluir/` | GET/POST | @login_required + dono |
| `inscrever` | `/eventos/<int:pk>/inscrever/` | POST | @login_required |
| `cancelar_inscricao` | `/eventos/<int:pk>/cancelar/` | POST | @login_required |
| `meus_eventos` | `/eventos/meus/` | GET | @login_required |

**Comportamentos obrigatórios:**

`lista_eventos` (RF07 — Busca/Filtro):
- Lê parâmetros GET: `q`, `categoria`, `status`
- Filtra queryset com `Q()` para busca por título ou descrição
- Filtra por categoria e status se informados
- Passa o `FormBusca` preenchido para o template

`criar_evento`:
- Salva `organizador=request.user` automaticamente (não expor no form)
- Redireciona para detalhe do evento após criação com mensagem de sucesso

`editar_evento` e `excluir_evento` (RF08):
- Verificar se `evento.organizador == request.user`
- Se não for o dono: retornar `HttpResponseForbidden` ou redirecionar com mensagem de erro

`inscrever`:
- Verificar se evento está ABERTO e não está lotado
- Usar `get_or_create` para evitar duplicatas
- Redirecionar para detalhe com mensagem de feedback

`cancelar_inscricao`:
- Deletar a inscrição se existir
- Redirecionar para detalhe com mensagem de feedback

---

## 7. URLs (urls.py)

### 7.1 `core/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('eventos.urls')),
]
```

### 7.2 `accounts/urls.py`
Todas as URLs devem ter `name=`:
```
name='cadastro'        → /accounts/cadastro/
name='login'           → /accounts/login/
name='logout'          → /accounts/logout/
name='perfil'          → /accounts/perfil/
```

Configurar em `settings.py`:
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'lista_eventos'
LOGOUT_REDIRECT_URL = 'login'
```

### 7.3 `eventos/urls.py`
Todas as URLs devem ter `name=`:
```
name='lista_eventos'      → /
name='detalhe_evento'     → /eventos/<int:pk>/
name='criar_evento'       → /eventos/criar/
name='editar_evento'      → /eventos/<int:pk>/editar/
name='excluir_evento'     → /eventos/<int:pk>/excluir/
name='inscrever'          → /eventos/<int:pk>/inscrever/
name='cancelar_inscricao' → /eventos/<int:pk>/cancelar/
name='meus_eventos'       → /eventos/meus/
```

---

## 8. TEMPLATES

### 8.1 `templates/base.html` (RF09 — herança de templates)

Deve conter:
- `<head>` com Bootstrap 5 via CDN e link para `style.css`
- `<nav>` com navegação:
  - Logo/nome do sistema à esquerda
  - Links: "Eventos", "Criar Evento" (se autenticado), "Meus Eventos" (se autenticado)
  - À direita: "Perfil" e "Sair" (se autenticado) ou "Entrar" e "Cadastrar" (se não)
- Bloco `{% block messages %}` que exibe `django.contrib.messages` com alertas Bootstrap
- Bloco `{% block content %}` para o conteúdo de cada página
- `<footer>` simples com nome do sistema e instituição

**Todos os outros templates devem começar com:**
```django
{% extends 'base.html' %}
{% block content %}
...
{% endblock %}
```

**Todas as URLs nos templates devem usar `{% url 'nome' %}`**, nunca caminhos hardcoded.

### 8.2 `accounts/templates/accounts/login.html`
- Formulário de login com campos `username` e `password`
- Link para a página de cadastro
- `{% csrf_token %}` obrigatório

### 8.3 `accounts/templates/accounts/cadastro.html`
- Formulário com os campos do `FormCadastro`
- Link para login
- `{% csrf_token %}` obrigatório

### 8.4 `accounts/templates/accounts/perfil.html`
- Exibe nome, username, email do usuário
- Formulário editável com campos do `FormPerfil`
- Lista de eventos em que o usuário está inscrito (nome do evento + data)

### 8.5 `eventos/templates/eventos/lista.html`
- Formulário de busca/filtro no topo (método GET)
- Grid de cards de eventos com: título, tipo, data de início, local, vagas disponíveis, status
- Badge colorido por status (verde=aberto, vermelho=encerrado, cinza=cancelado)
- Link para o detalhe de cada evento
- Mensagem "Nenhum evento encontrado" se queryset vazio

### 8.6 `eventos/templates/eventos/detalhe.html`
- Todos os campos do evento exibidos
- Lista de categorias como badges
- Contador de vagas disponíveis
- Botão "Inscrever-se" (se usuário autenticado, evento aberto e não inscrito)
- Botão "Cancelar Inscrição" (se já inscrito)
- Botões "Editar" e "Excluir" apenas se `request.user == evento.organizador`
- Lista dos participantes inscritos (apenas nome) — visível para o organizador

### 8.7 `eventos/templates/eventos/criar.html` e `editar.html`
- Formulário `FormEvento` renderizado
- Botão de salvar e link de cancelar
- `{% csrf_token %}` obrigatório

### 8.8 `eventos/templates/eventos/confirmar_exclusao.html`
- Mensagem de confirmação: "Tem certeza que deseja excluir o evento X?"
- Botão confirmar (POST) e botão cancelar (link GET para detalhe)

---

## 9. SETTINGS.PY — CONFIGURAÇÕES IMPORTANTES

```python
INSTALLED_APPS = [
    # apps padrão Django...
    'accounts',
    'eventos',
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Maceio'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'lista_eventos'
LOGOUT_REDIRECT_URL = 'login'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

TEMPLATES = [{
    ...
    'DIRS': [BASE_DIR / 'templates'],  # importante para o base.html global
    ...
}]
```

---

## 10. MIGRATIONS E DADOS DE EXEMPLO (RF10)

### 10.1 Ordem de execução das migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations eventos
python manage.py migrate
```

### 10.2 Fixture `fixtures/dados_iniciais.json`

Criar um arquivo de fixture com:
- 2 usuários comuns (ex: `aluno1`, `aluno2`) com senha `senha1234`
- 1 usuário organizador (ex: `organizador1`) com senha `senha1234`
- 3 categorias: `Extensão`, `Pesquisa`, `Cultura`
- 4 eventos variados (tipos e status diferentes)
- 3 inscrições de exemplo

Comando para carregar:
```bash
python manage.py loaddata fixtures/dados_iniciais.json
```

Ou criar um `management command` em `eventos/management/commands/seed.py` que popula o banco programaticamente:
```bash
python manage.py seed
```

---

## 11. ADMIN (admin.py)

Registrar todos os modelos no admin do Django para facilitar a avaliação:

```python
# eventos/admin.py
admin.site.register(Categoria)
admin.site.register(Evento)
admin.site.register(Inscricao)

# accounts/admin.py
admin.site.register(Perfil)
```

Criar um superusuário:
```bash
python manage.py createsuperuser
# username: admin | senha: admin1234
```

---

## 12. SEGURANÇA (RF08 + RNF 5.4)

- **CSRF:** nunca remover `{% csrf_token %}` de nenhum formulário POST
- **Senhas:** usar apenas o sistema nativo do Django (`UserCreationForm`, `authenticate`) — nunca salvar senha em texto puro
- **@login_required:** aplicar em todas as views de CRUD, inscrição, perfil e meus_eventos
- **Verificação de dono:** nas views `editar_evento` e `excluir_evento`, após o `get_object_or_404`, verificar:
  ```python
  if evento.organizador != request.user:
      messages.error(request, 'Você não tem permissão para isso.')
      return redirect('detalhe_evento', pk=evento.pk)
  ```

---

## 13. QUALIDADE DE CÓDIGO (RNF 5.2)

- Nenhuma lógica de negócio nos templates — apenas exibição e condicionais simples
- Métodos de negócio ficam no `model` (ex: `vagas_disponiveis`, `esta_lotado`)
- Views devem ser enxutas: recebem request, chamam model/form, retornam response
- Nomenclatura em português ou inglês — escolher um e manter consistente
- Indentação: 4 espaços, seguindo PEP 8

---

## 14. ARQUIVOS OBRIGATÓRIOS DE ENTREGA

### `requirements.txt`
Gerar com:
```bash
pip freeze > requirements.txt
```
Deve conter no mínimo: `Django>=4.2`

### `.gitignore`
```
__pycache__/
*.pyc
.env
db.sqlite3
venv/
.venv/
*.egg-info/
```

### `README.md`
Deve conter obrigatoriamente:
1. Nome do projeto e descrição do contexto
2. Nomes completos dos integrantes
3. Instruções passo a passo para execução local:
   ```bash
   git clone ...
   cd eventoifs
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py loaddata fixtures/dados_iniciais.json
   python manage.py runserver
   ```
4. Lista dos requisitos funcionais implementados (RF01 a RF10)
5. Pelo menos 2 capturas de tela da aplicação funcionando

---

## 15. CHECKLIST FINAL (para o agente verificar antes de encerrar)

- [ ] App `accounts` e app `eventos` criados e registrados em `INSTALLED_APPS`
- [ ] Modelo `Evento` com mínimo de 5 campos relevantes
- [ ] Relacionamento `ForeignKey` (Evento → User) e `ManyToMany` (Evento → Categoria) implementados
- [ ] CRUD completo funcionando (listar, criar, editar, excluir)
- [ ] Formulário com validação personalizada em pelo menos 1 campo
- [ ] Busca/filtro via parâmetro GET funcionando
- [ ] `@login_required` em todas as views protegidas
- [ ] Verificação de dono antes de editar/excluir
- [ ] `base.html` com herança em todos os templates
- [ ] Django Messages exibindo feedbacks ao usuário
- [ ] Todas as URLs com `name=` e referenciadas com `{% url %}` nos templates
- [ ] Migrations geradas e aplicadas
- [ ] Fixture ou seed com dados de exemplo
- [ ] `requirements.txt`, `.gitignore` e `README.md` presentes
- [ ] CSRF ativo em todos os formulários POST
- [ ] Senhas tratadas via sistema nativo do Django
