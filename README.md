# MeetRox

Uma aplicação web robusta construída com Django, oferecendo autenticação completa, gerenciamento de perfis de usuários e integração com CRM (HubSpot). O projeto está otimizado para execução via Docker e inclui ferramentas para desenvolvimento, testes e deploy em produção.

## Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
  - [Modo Local](#modo-local-sem-docker)
  - [Com Docker](#execução-com-docker-recomendado)
- [Configuração](#configuração)
- [Testes e Qualidade de Código](#testes-e-qualidade-de-código)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)

## Visão Geral

MeetRox é uma aplicação backend completa desenvolvida em Django 5.2 com Django REST Framework, projetada para gerenciar usuários, autenticação JWT e integração com sistemas de CRM. O projeto segue boas práticas de desenvolvimento, incluindo histórico de mudanças em modelos, validação de dados e documentação automática da API.

## Tecnologias

- **Python 3.10+**
- **Django 5.2**
- **Django REST Framework 3.15.2**
- **PostgreSQL 17**
- **JWT Authentication** (SimpleJWT)
- **Docker & Docker Compose**
- **Poetry** (gerenciamento de dependências)
- **Gunicorn** (servidor WSGI para produção)
- **drf-yasg** (documentação Swagger/OpenAPI)
- **pytest-django** (testes)
- **black/isort/flake8** (lint e formatação)

## Funcionalidades

### Autenticação e Perfis

- Modelo de usuário customizado (`Profile`) estendendo `AbstractUser`
- Sistema de tipos de perfil: Administrador, Desenvolvedor e Usuário CRM
- Autenticação JWT com tokens de acesso, refresh, verify e blacklist
- Histórico completo de alterações em perfis (django-simple-history)
- Sistema de grupos e permissões personalizadas

### Integração com CRM

- Módulo `crm_integration` para integração com HubSpot API
- Sistema de pré-cadastro (`PreSignUp`) para capturar dados de contatos do CRM
- Armazenamento de dados CRM em formato JSON
- Rastreamento de origem e status de conclusão de cadastros
- Suporte para múltiplas fontes de CRM

### Infraestrutura

- Docker Compose com serviços Django e PostgreSQL
- Modo desenvolvimento e produção (Gunicorn)
- Coleta automática de arquivos estáticos
- Migrations automáticas no startup
- Criação automática de superusuário admin
- CORS configurado para integrações frontend

## Requisitos

- **Python** >= 3.10 (recomendado: 3.14)
- **Poetry** (gerenciador de dependências)
- **Docker** e **Docker Compose** (recomendado)
- **PostgreSQL 17** (quando não usar Docker)

As dependências Python estão gerenciadas via Poetry no arquivo `service/pyproject.toml`.

## Instalação

### Modo Local (sem Docker)

1. Clone o repositório:

```bash
git clone https://github.com/devdinho/meetrox.git
cd meetrox
```

2. Crie e ative um ambiente virtual Python >=3.10:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

3. Instale o Poetry e as dependências:

```bash
pip install poetry
cd service
poetry install
```

4. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Database
POSTGRES_USER=meetrox_user
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_DB=meetrox_db
DB_PORT=5432

# Django
ADMIN_PASSWORD=senha_admin_segura
SECRET_KEY=sua_secret_key_django
DEBUG=True
PRODUCTION=False

# CORS (opcional)
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

5. Execute as migrations e crie o banco de dados:

```bash
cd service/src
python manage.py migrate
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver 0.0.0.0:8003
```

Acesse em: http://localhost:8003/

### Execução com Docker (recomendado)

O projeto fornece um `Dockerfile` e `docker-compose.yaml` que configuram automaticamente todos os serviços necessários.

1. Clone o repositório:

```bash
git clone https://github.com/devdinho/meetrox.git
cd meetrox
```

2. Configure o arquivo `.env` na raiz (veja exemplo acima)

3. Inicie os containers:

```bash
docker compose up --build
```

O serviço estará disponível em: http://localhost:8003/

**O que acontece no startup do container:**

- ✅ Coleta de arquivos estáticos
- ✅ Geração e aplicação de migrations
- ✅ Criação automática do superusuário `admin` (usando `ADMIN_PASSWORD`)
- ✅ Inicialização do servidor (Gunicorn em produção, runserver em dev)

## Configuração

### Variáveis de Ambiente

| Variável            | Descrição                    | Padrão     | Obrigatória |
| ------------------- | ---------------------------- | ---------- | ----------- |
| `POSTGRES_USER`     | Usuário do PostgreSQL        | -          | ✅          |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL          | -          | ✅          |
| `POSTGRES_DB`       | Nome do banco de dados       | meetrox_db | ❌          |
| `DB_PORT`           | Porta do PostgreSQL          | 5432       | ❌          |
| `ADMIN_PASSWORD`    | Senha do superusuário admin  | -          | ✅          |
| `SECRET_KEY`        | Secret key do Django         | -          | ✅          |
| `DEBUG`             | Modo debug do Django         | False      | ❌          |
| `PRODUCTION`        | Modo produção (usa Gunicorn) | False      | ❌          |
| `ALLOWED_HOSTS`     | Hosts permitidos             | localhost  | ❌          |

### Modos de Execução

- **Desenvolvimento**: `PRODUCTION=False` → usa `runserver` do Django
- **Produção**: `PRODUCTION=True` → usa Gunicorn com configurações otimizadas

## Testes e Qualidade de Código

### Executar Testes

```bash
# Dentro do container ou no diretório service/
./scripts/run_unit_tests.sh
```

Ou usando pytest diretamente:

```bash
cd service/src
pytest
```

### Lint e Formatação

Execute black, isort e flake8:

```bash
./scripts/start-lint.sh src/
```

Ou individualmente:

```bash
cd service/src
black .
isort .
flake8 .
```

## Estrutura do Projeto

```
meetrox/
├── docker-compose.yaml          # Configuração dos serviços Docker
├── credentials                  # Notas sobre integração CRM (não expor)
├── LICENSE                      # Licença MIT
├── README.md                    # Este arquivo
└── service/
    ├── Dockerfile               # Imagem Docker do serviço
    ├── pyproject.toml           # Dependências Poetry
    ├── poetry.lock
    ├── scripts/
    │   ├── start.sh             # Script de inicialização
    │   ├── run_unit_tests.sh    # Execução de testes
    │   └── start-lint.sh        # Lint e formatação
    └── src/
        ├── manage.py
        ├── gunicorn_config.py   # Configuração Gunicorn
        ├── authentication/      # App de autenticação
        │   ├── models/
        │   │   ├── Profile.py          # Modelo de usuário customizado
        │   │   └── Groups.py
        │   ├── api/
        │   │   ├── ProfileRestView.py  # ViewSet de perfis
        │   │   └── CreateProfileRestView.py
        │   ├── serializers/
        │   ├── admin/
        │   ├── migrations/
        │   └── tests/
        ├── crm_integration/     # App de integração CRM
        │   ├── models/
        │   │   ├── Crm_Integration.py
        │   │   └── PreSignUp.py        # Modelo de pré-cadastro
        │   ├── api/
        │   │   └── v1/
        │   │       └── PreSignUpApiView.py
        │   ├── serializers/
        │   ├── admin/
        │   └── migrations/
        ├── meetrox/             # Configurações do projeto
        │   ├── settings/
        │   │   ├── base.py
        │   │   └── env.py
        │   ├── urls.py          # Rotas principais
        │   ├── wsgi.py
        │   └── asgi.py
        ├── utils/               # Utilidades
        │   ├── constants.py     # Constantes (ProfileType, Status)
        │   └── cache_utils.py
        └── static/              # Arquivos estáticos
```

## API Endpoints

### Autenticação (JWT)

| Método | Endpoint              | Descrição                       |
| ------ | --------------------- | ------------------------------- |
| POST   | `/api/login/`         | Obter token de acesso e refresh |
| POST   | `/api/login/refresh/` | Renovar token de acesso         |
| POST   | `/api/login/verify/`  | Verificar validade do token     |
| POST   | `/api/logout/`        | Blacklist do token (logout)     |

### Perfis de Usuário

| Método    | Endpoint             | Descrição                   |
| --------- | -------------------- | --------------------------- |
| POST      | `/api/register/`     | Criar novo perfil           |
| GET       | `/api/profile/`      | Listar perfis (autenticado) |
| GET       | `/api/profile/{id}/` | Detalhar perfil específico  |
| PUT/PATCH | `/api/profile/{id}/` | Atualizar perfil            |

### Integração CRM

| Método | Endpoint                                 | Descrição             |
| ------ | ---------------------------------------- | --------------------- |
| POST   | `/api/crm-integration/pre-sign-up/`      | Criar pré-cadastro    |
| GET    | `/api/crm-integration/pre-sign-up/`      | Listar pré-cadastros  |
| GET    | `/api/crm-integration/pre-sign-up/{id}/` | Detalhar pré-cadastro |

### Documentação (apenas em desenvolvimento)

| Endpoint    | Descrição            |
| ----------- | -------------------- |
| `/swagger/` | Interface Swagger UI |
| `/redoc/`   | Documentação ReDoc   |

### Diretrizes

- ✅ Execute os testes antes de abrir PR: `./scripts/run_unit_tests.sh`
- ✅ Siga as regras de lint: `./scripts/start-lint.sh src/`
- ✅ Escreva mensagens de commit descritivas
- ✅ Adicione testes para novas funcionalidades
- ✅ Atualize a documentação quando necessário

## Comandos Úteis

```bash
# Docker
docker compose up --build              # Subir serviços
docker compose down                    # Parar serviços
docker compose logs -f meetrox_service          # Ver logs do Django
docker exec -it meetrox_service bash   # Acessar container

# Django (modo local)
python service/src/manage.py migrate                # Aplicar migrations
python service/src/manage.py createsuperuser       # Criar superusuário
python service/src/manage.py makemigrations        # Criar migrations
python service/src/manage.py shell                 # Shell interativo
python service/src/manage.py collectstatic         # Coletar estáticos

# Testes e Lint
./service/scripts/run_unit_tests.sh    # Executar testes
./service/scripts/start-lint.sh src/   # Executar lint
```

## Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido por:** Anderson Freitas (freitas.dev@proton.me)  
**Repositório:** [github.com/devdinho/meetrox](https://github.com/devdinho/meetrox)
