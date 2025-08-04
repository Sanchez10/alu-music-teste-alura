# Alu Music - Teste de Desenvolvedor Python com LLMs

Este projeto é parte de um desafio técnico para vaga de Python com foco em LLMs. A aplicação permite ingestão, classificação e análise de comentários sobre músicas, shows e álbuns.

---

## Tecnologias Utilizadas

- Python 3.10.10
- Flask
- PostgreSQL (via Docker)
- SQLAlchemy
- JWT (autenticação)
- Docker + Docker Compose

---

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Sanchez10/alu-music-teste-alura.git
cd alu-music-teste-alura
```

### 2. Crie o arquivo .env

Crie um arquivo .env com o seguinte conteúdo:

```bash
DATABASE_URL=postgresql://user:pass@db:5432/alu_music
SECRET_KEY=supersecret
```

### 3. Subar os containers com Docker

```bash
docker compose up --build
```

### 4. Crie as tabelas do banco

```bash
docker compose run --rm web python scripts/create_tables.py
```

### 5. Gere um JWT válido para testes

```bash
docker compose run --rm web python scripts/generate_token.py
```

Copie o token exibido no terminal e use como **Bearer** nos headers das requisições.

## Testes de API

### POST /api/comentarios/

Adiciona um novo comentário.

**Header:**

```http
Authorization: Bearer <seu_token>
Content-Type: application/json
```

**Body:**

```http
{
    "texto": "Essa música é muito boa!"
}
```

### GET /api/comentarios/

Lista todos os comentários existentes.

**Header:**

```http
Authorization: Bearer <seu_token>
Content-Type: application/json
```

## Estrutura de Pastas

```bash
app/
├── models/              # Modelos SQLAlchemy
├── routes/              # Rotas Flask (Blueprints)
├── services/            # Classificador LLM (simulado)
├── utils/               # Autenticação
scripts/                 # Scripts auxiliares
tests/                   # Testes (em breve)
```
