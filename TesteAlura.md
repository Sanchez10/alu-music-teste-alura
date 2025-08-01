# Teste vaga de Python com foco em LLM | Alura

Olá! Que bom ter você por aqui 🚀

Alguns pontos estão propositadamente abertos para avaliarmos seu raciocínio. Anote qualquer dúvida e registre as decisões de arquitetura que tomar.

---

## Tecnologias **obrigatórias**

| Camada       | Requisitos                                                      |
| ------------ | --------------------------------------------------------------- |
| Execução     | Python ≥ 3.10  •  Docker                                        |
| Web          | Flask                                                           |
| Persistência | SQL (MySQL ou PostgreSQL)                                       |
| LLM          | modelo à sua escolha                                            |
| Testes       | PyTest cobrindo unidades **e** integrações                      |
| CI/CD        | Git + GitHub • GitHub Actions **acionado por pipeline Jenkins** |

> O pipeline do Jenkins deve iniciar o workflow do GitHub Actions e exibir o resultado — demonstre isso no Jenkinsfile e no README.

---

## Avaliação

| Eixo                        | O que observaremos                                               |
| --------------------------- | ---------------------------------------------------------------- |
| **Qualidade técnica**       | arquitetura, clareza de código, testes, paralelismo              |
| **Derivação de requisitos** | hipóteses registradas, justificativas                            |
| **Organização**             | estrutura de pastas, granularidade de commits, documentação      |
| **Dev Experience**          | ambiente Docker simples de subir, CI verde, comandos utilitários |
| **Evals**                   | métricas automatizadas que mostrem a qualidade da classificação  |

---

## Entrega

1. Repositório no GitHub (público ou privado). Se privado, adicione:
   - [lucasboot](https://github.com/lucasboot)
2. **README** explicando:
   - Como levantar tudo via Docker
   - Como rodar testes e evals
   - Como acompanhar cada etapa dos pipelines
   - Principais decisões de design

---

# Sobre o desafio

## Cenário

A **AluMusic** acompanha milhares de comentários deixados por ouvintes sobre artistas, álbuns, clipes e shows. O time de curadoria musical precisa de sinais rápidos sobre o que está gerando hype, insatisfação ou dúvidas no público.

Sua missão é criar um serviço que **receba, classifique e analise** esses comentários, oferecendo:

1. um endpoint autenticado para ingestão;

2. um painel privado para a equipe de curadoria;

3. um relatório público em tempo real;

4. um resumo semanal automatizado por e‑mail.

---

### 1. Classificação de Comentários

- **Entrada**: `id` (UUID) + `texto`, enviados individualmente ou em lote.
- **Saída**:
  - `categoria` ∈ { **ELOGIO**, **CRÍTICA**, **SUGESTÃO**, **DÚVIDA**, **SPAM** }
  - `tags_funcionalidades` (lista: código + explicação — ex.: `feat_autotune`, `clip_narrativa`, `show_duração`)
  - `confianca` (0‑1)
- Deve haver autenticação (JWT, sessão, etc.) no endpoint `/api/comentarios`.
- Lotes grandes devem ser processados em paralelo.

---

### 2. Relatório em tempo real

Rota pública `/relatorio/semana` devolvendo **cinco gráficos obrigatórios** (HTML ou imagem embutida) e/ou JSON correspondente, atualizados no máximo a cada 60 s. Os gráficos devem trazer insights relevantes — por exemplo:

- Categorias mais frequentes por artista
- Evolução de críticas após lançamento
- Tags mais citadas nas últimas 48h

---

### 3. Dashboard privado

Interface com login para:

- Pesquisar e filtrar comentários por artista, álbum, tag ou categoria
- Ver histórico de classificações
- Exportar dados

---

### 4. Resumo semanal por e‑mail

Ao final de cada semana:

1. Gerar texto com LLM destacando tendências
2. Enviar automaticamente aos stakeholders
3. Armazenar o resumo na base de dados

---

### 5. Evals & Métricas

- Defina critérios de avaliação do modelo de classificação (recall para SPAM, por exemplo).
- Deixe um comando único que rode os evals e gere um relatório de métricas. O CI deve falhar se os resultados ficarem abaixo de um patamar mínimo definido por você.

---

### 6. Extra (não obrigatório)

**Mini Insight‑Q&A**

Adicione uma rota autenticada `/insights/perguntar` (HTTP POST) onde stakeholders possam enviar **uma pergunta curta em linguagem natural** sobre os feedbacks das **últimas 8 semanas**.

**Fluxo mínimo**

1. Ao receber a pergunta, a aplicação seleciona os **três resumos semanais** mais recentes.
2. Concatena esses resumos como contexto e chama a LLM para responder em até **150 palavras**.
3. A resposta deve conter:
   - Texto gerado pela LLM.
   - Lista das semanas citadas como fonte (ex.: `[“2025‑W30”, “2025‑W29”]`).
4. Retorne tudo em JSON.

---

Boa sorte! Estamos ansiosos para ver como você vai evoluir este desafio 🔥
