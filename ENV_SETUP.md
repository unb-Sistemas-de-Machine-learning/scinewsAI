# Configuração de Variáveis de Ambiente

Este documento descreve como configurar as variáveis de ambiente para o SciNewsAI.

## Frontend

### Criando o arquivo `.env`

1. Copie o arquivo `.env.example`:
```bash
cp web/frontend/.env.example web/frontend/.env
```

2. Configure as variáveis conforme necessário:
```
# API Configuration
VITE_API_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=SciNewsAI
VITE_APP_TITLE=SciNewsAI - Notícias de Ciência da Computação
```

### Variáveis disponíveis

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `VITE_API_URL` | URL base da API backend | `http://localhost:8000` |
| `VITE_APP_NAME` | Nome da aplicação | `SciNewsAI` |
| `VITE_APP_TITLE` | Título da aplicação (título da página) | `SciNewsAI - Notícias de Ciência da Computação` |

## Backend

### Criando o arquivo `.env`

1. Copie o arquivo `.env.example`:
```bash
cp web/backend/.env.example web/backend/.env
```

2. Configure as variáveis conforme necessário:
```
# Application Settings
APP_NAME=SciNewsAI
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/scinewsai

# Redis Configuration (optional)
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:8080

# External APIs
ARXIV_API_URL=http://export.arxiv.org/api/query

# AI/LLM Configuration
OPENAI_API_KEY=
GEMINI_API_KEY=

# Email Configuration
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=noreply@scinewsai.com
```

### Variáveis disponíveis

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `APP_NAME` | Nome da aplicação | `SciNewsAI` | ❌ |
| `DEBUG` | Modo debug (true/false) | `false` | ❌ |
| `DATABASE_URL` | URL de conexão PostgreSQL | `postgresql://postgres:postgres@db:5432/scinewsai` | ✅ |
| `REDIS_URL` | URL do Redis | `redis://redis:6379/0` | ❌ |
| `SECRET_KEY` | Chave secreta para JWT | `your-super-secret-key-change-in-production` | ✅ |
| `ALGORITHM` | Algoritmo de encriptação JWT | `HS256` | ❌ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token de acesso (minutos) | `30` | ❌ |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Tempo de expiração do token de refresh (dias) | `7` | ❌ |
| `CORS_ORIGINS` | Origins permitidas (separadas por vírgula) | Localhost em múltiplas portas | ❌ |
| `ARXIV_API_URL` | URL da API ArXiv | `http://export.arxiv.org/api/query` | ❌ |
| `OPENAI_API_KEY` | Chave da API OpenAI | ` ` | ❌ |
| `GEMINI_API_KEY` | Chave da API Google Gemini | ` ` | ❌ |
| `SMTP_HOST` | Host do servidor SMTP | ` ` | ❌ |
| `SMTP_PORT` | Porta do servidor SMTP | `587` | ❌ |
| `SMTP_USER` | Usuário SMTP | ` ` | ❌ |
| `SMTP_PASSWORD` | Senha SMTP | ` ` | ❌ |
| `EMAIL_FROM` | Email para envios | `noreply@scinewsai.com` | ❌ |

## Docker Compose

O arquivo `docker-compose.yml` foi configurado para usar os arquivos `.env` de forma automática:

```yaml
backend:
  env_file:
    - ./backend/.env

frontend:
  env_file:
    - ./frontend/.env
```

## Iniciar o projeto

### Com Docker Compose

```bash
docker-compose up -d
```

As variáveis de ambiente serão carregadas automaticamente dos arquivos `.env`.

### Modo desenvolvimento (sem Docker)

#### Backend
```bash
cd web/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd web/frontend
npm install
npm run dev
```

## Variáveis de ambiente para Produção

Para produção, você deve:

1. **Mudar `SECRET_KEY`**: Gere uma chave secreta forte
   ```bash
   openssl rand -hex 32
   ```

2. **Mudar `DEBUG`**: Defina como `false`

3. **Atualizar `CORS_ORIGINS`**: Use apenas os domínios de produção

4. **Configurar APIs externas**: 
   - `OPENAI_API_KEY`: Se usar OpenAI
   - `GEMINI_API_KEY`: Se usar Google Gemini
   - `SMTP_*`: Se quiser enviar emails

5. **Banco de dados**: Use um PostgreSQL gerenciado ou com backup

## Problemas comuns

### Erro "no such file or directory: '.env'"
- Certifique-se de que criou o arquivo `.env` antes de iniciar os containers

### Erro de conexão com banco de dados
- Verifique se a `DATABASE_URL` está correta
- Aguarde o PostgreSQL estar pronto (use `depends_on` com healthcheck)

### CORS errors no frontend
- Adicione a URL do frontend em `CORS_ORIGINS` no backend
- Exemplo: `CORS_ORIGINS=...,http://meu-dominio.com`
