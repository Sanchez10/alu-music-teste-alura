# Alu Music - Teste Python com LLMs

Este projeto foi desenvolvido como parte de um desafio técnico Python com foco em LLMs. A aplicação permite ingestão, classificação e análise de comentários sobre músicas, shows e álbuns. Ao longo do desenvolvimento, buscou-se atender requisitos funcionais e não funcionais utilizando boas práticas de engenharia de software, integração com modelos de linguagem, CI/CD e ferramentas modernas de visualização e persistência.

## ✨ Visão Geral e Arquitetura

A arquitetura do projeto segue os princípios de separação de responsabilidades, com estrutura modular em Blueprints do Flask. Foi adotada uma estrutura MVC simplificada:

- **Models (SQLAlchemy):** Comentário, ResumoSemanal e UserFake
- **Routes (Blueprints):** Comentários, Dashboard, Relatório e Resumo
- **Services:** Classificador com LLM e rotina de geração de resumo semanal
- **Utils:** Middleware de autenticação
- **Frontend:** Templates Jinja2 simples para dashboard privado

### 🔧 Trade-offs e Decisões Técnicas

- **LLM local (TinyLLaMA via Ollama):** Foi utilizado TinyLLaMA devido ao bom desempenho local e facilidade de uso com a API do Ollama. Como trade-off, temos menor capacidade sem GPU (apesar de que usando CUDAs fica muito melhor), mas mais controle e segurança dos dados.

- **Persistência com PostgreSQL via Docker:** Oferece confiabilidade e integração com SQLAlchemy. Optou-se por `docker-compose` para facilitar setup e isolar dependências.

- **Agendamento com APScheduler:** Executa a tarefa de resumo semanal sem depender de cron externo. Como cuidado, iniciamos o scheduler apenas fora do modo `TESTING`.

- **SMTP nativo:** Foi escolhido por simplicidade, mas poderia ser substituído por SendGrid para produção.

- **Autenticação mista:** JWT para API e sessão com Flask-Login para dashboard. Essa separação atende múltiplos tipos de cliente (frontend web, ferramentas de API, etc).

- **CI/CD com GitHub Actions + Jenkins:** Combinou-se os dois para validar testes, cobertura e integração contínua. Jenkins atua como orquestrador que dispara os workflows do GitHub.

## 📦 Tecnologias Utilizadas

- Python 3.10
- Flask + SQLAlchemy
- PostgreSQL (via Docker)
- Ollama + TinyLLaMA (modelo local)
- APScheduler (tarefas periódicas)
- SMTP nativo (envio de email)
- Chart.js (visualização)
- Flask-Login + JWT
- Pytest + Coverage + GitHub Actions + Jenkins

## 🚀 Funcionalidades Implementadas

### 🔎 Classificação de Comentários com LLM

- POST `/api/comentarios/` permite o envio de comentários
- GET `/api/comentarios/` retorna todos os comentários feitos
- A LLM classifica automaticamente:
  - **categoria** (ex: crítica, sugestão, elogio)
  - **tags_funcionalidades** (ex: artista, palco, som)
  - **confianca** (nível de certeza)

### 📊 Relatório em Tempo Real

- Rota pública: `/relatorio/semana`
- Gráficos interativos com Chart.js:
  - Tags mais citadas
  - Evolução de categorias nos últimos 7 dias
- Atualiza a cada 60 segundos com cache

### 🔐 3. Dashboard Privado

- Acesso via login com senha
- Visualização de comentários com filtros
  - Filtro por categoria e tags
- Exportação de CSV dos dados visíveis
- Protegido por sessão com Flask-Login

### 🧠 4. Resumo Semanal com LLM

- Agrupa todos os comentários da última semana
- Gera resumo via LLM (TinyLLaMA)
- Armazena em tabela `resumos_semanal`
- Envia automaticamente por email

### ❓ 5. Insights com LLM (Q&A)

- Rota: `/insights/perguntar`
- Permite perguntar sobre os resumos anteriores
- Usa LLM para retornar resposta contextual baseada em múltiplos resumos armazenados

## 🧪 Testes Automatizados

- Testes unitários (Pytest)
- Cobertura com pytest-cov
- Separação por jobs no CI:
  - Testes unitários
  - Testes de métricas
  - Testes de integração

## Execução local

```bash
pytest --cov=app tests/
```

## 🔄 CI/CD com GitHub Actions + Jenkins

- `pytest` e `coverage` validados em cada push
- Jenkins orquestra o pipeline e monitora qualidade
- Fails no pull request se cobertura < 80% ou testes falharem

## 🧰 Setup do Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Sanchez10/alu-music-teste-alura.git
cd alu-music-teste-alura
```

### 2. Crie o arquivo .env

```bash
DATABASE_URL=postgresql://user:pass@db:5432/alu_music
SECRET_KEY=supersecret
EMAIL_USER=joao.sanchez01@gmail.com
EMAIL_PASS=sua_senha_aqui
```

### 3. Suba os containers

```bash
docker compose up --build
```

### 4. Crie as tabelas do banco

```bash
docker compose run --rm web python -m scripts.create_tables.py
```

### 5. Rode as migrations

```bash
flask db upgrade
```

### 6. Gere token JWT (para testes)

```bash
docker compose run --rm web python -m scripts.generate_token.py
```

## 🧠 Modelo de LLM

A ideia é utilizar uma LLM open source e que possa rodar localmente, ou seja, tendo um funcionamento inclusive offline. Para isso escolhi o Ollama, mais especificamente o motor "Tinyllama", e então devemos baixá-la e rodar localmente.

https://ollama.com/download

```bash
ollama pull tinyllama
```

```bash
ollama serve
```

Como estamos usando docker é necessário abrir o WSL no Windows, caso ainda não tenha instalado e descobri a refeência do IP da sua máquina host, para apontar corretamente a requisição da API do Ollama. Rode o seguinte commando no WSL

```bash
ip route | grep default
```

E então faremos uma integração para acessar o modelo via **HOST_IP:11434** usando Python

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

## 📊 Relatório Gráfico

- Disponível em /relatorio/semana
- Atualização dinâmica a cada 60s

## 🔐 Dashboard Privado

- Login em /login
- Visualização em /dashboard
- Exportação de CSV

  ### Acesse a dashboard (http://localhost:5000/login)

  Login com a senha: `admin123`

## 📬 Email de Resumo Semanal

- Executado automaticamente via APScheduler
- Pode ser testado manualmente via:

```bash
flask shell
>>> from app.services.resumo import gerar_e_enviar_resumo
>>> gerar_e_enviar_resumo()
```

### Acesse o relatório semanal (http://localhost:5000/relatorio/semana)

## 📁 Estrutura de Pastas

```bash
app/
├── models/              # Modelos SQLAlchemy
├── routes/              # Rotas Flask (Blueprints)
├── services/            # Classificador LLM (simulado)
├── utils/               # Autenticação
scripts/                 # Scripts auxiliares
tests/                   # Testes (em breve)
```
