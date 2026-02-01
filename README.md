# Teste de Entrada - Intuitive Care

**Candidato:** João Vitor Vale da Cruz

🚀 **Demo:** https://teste-intuitive-care-deploy.vercel.app

## Visão Geral

Pipeline ETL completo para demonstrações contábeis da ANS, com API REST e interface web.

### Entregáveis

| Componente | Descrição |
|------------|-----------|
| `data/output/consolidado_despesas.csv` | Despesas consolidadas dos 3 trimestres |
| `data/output/despesas_agregadas.csv` | Despesas agregadas por operadora/UF |
| `data/output/Teste_Joao_Vitor_Vale_da_Cruz.zip` | CSV agregado compactado |
| API FastAPI | Endpoints REST para consulta |
| Frontend Vue 3 | Interface com tabela, busca e gráficos |

## Requisitos

- **Python** 3.10+
- **Node.js** 18+
- **PostgreSQL** 13+

## Execução Rápida

```bash
# 1. Configurar ambiente Python
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Executar pipeline ETL
python main.py

# 3. Configurar banco (PostgreSQL)
psql -U postgres -d tst_ans -f sql/02_ddl.sql
psql -U postgres -d tst_ans -f sql/03_import.sql

# 4. Iniciar API
uvicorn backend.main:app --reload

# 5. Iniciar frontend (em outro terminal)
cd frontend
npm install
npm run dev
```

## Passo a Passo Detalhado

### 1) Pipeline de Dados (Python)

```bash
# Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar pipeline ETL
python main.py
```

**Saída esperada:**
```
============================================================
PIPELINE ETL - DEMONSTRAÇÕES CONTÁBEIS ANS
============================================================

[1/6] Identificando os últimos trimestres disponíveis...
[2/6] Baixando arquivos ZIP...
[3/6] Extraindo arquivos ZIP...
[4/6] Processando arquivos extraídos...
[5/6] Enriquecendo dados com cadastro das operadoras...
[6/6] Validando e agregando dados...

============================================================
PIPELINE FINALIZADO COM SUCESSO!
============================================================
```

**Arquivos gerados** (`data/output/`):
- `consolidado_despesas.zip` - Dados brutos consolidados
- `despesas_agregadas.csv` - Dados agregados por operadora/UF
- `operadoras_ativas.csv` - Cadastro de operadoras (download)
- `Teste_Joao_Vitor_Vale_da_Cruz.zip` - Entregável final

### 2) Banco de Dados (PostgreSQL)

```bash
# Criar banco de dados
createdb -U postgres tst_ans

# Criar tabelas
psql -U postgres -d tst_ans -f sql/02_ddl.sql

# Importar dados
psql -U postgres -d tst_ans -f sql/03_import.sql
```

**Variável de ambiente** (opcional):
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/tst_ans"
```

### 3) API (FastAPI)

```bash
uvicorn backend.main:app --reload
```

**Endpoints:**

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/operadoras` | Lista operadoras (paginado) |
| GET | `/api/operadoras/{cnpj}` | Detalhes de uma operadora |
| GET | `/api/operadoras/{cnpj}/despesas` | Histórico de despesas |
| GET | `/api/operadoras/estatisticas/despesas-uf` | Despesas por UF |
| GET | `/api/estatisticas` | Estatísticas agregadas |

### 4) Frontend (Vue 3 + Vite)

```bash
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:5173`

> A aplicação assume a API em `http://127.0.0.1:8000`.

## Trade-offs e Decisões Técnicas

### Pipeline ETL

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Processamento | Em memória | Simples para volume dos 3 trimestres |
| Join | Por `REG_ANS` | CNPJ não existe nos demonstrativos |
| Registros sem match | `INNER JOIN` | Evita dados incompletos |
| CNPJ inválido | Descartar | Garante qualidade dos dados |
| Valores <= 0 | Manter na consolidação | Removidos na validação final |

### Banco de Dados

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Normalização | Tabelas separadas | Evita duplicação |
| Valores monetários | `NUMERIC(18,2)` | Precisão financeira |
| Datas | `DATE` | Semântica correta |

### API

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Framework | FastAPI | Tipagem, docs automáticas |
| Paginação | Offset-based | Simples para ~1000 operadoras |
| Cache | Em memória (5min) | Reduz carga no banco |
| Resposta | Com metadados | Facilita UI |

### Frontend

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Estado | Pinia | Recomendado Vue 3 |
| Busca | Server-side | Garante todos os resultados |
| Gráficos | Chart.js | Leve e flexível |
| Erros | Alertas visuais | Feedback claro |

## Conformidade com o Enunciado

| Item | Status | Observação |
|------|--------|------------|
| 1.1 Download API ANS | OK | 3 últimos trimestres |
| 1.2 Processamento | OK | Resiliente a formatos |
| 1.3 Consolidação | OK | CSV + ZIP |
| 2.1 Validação | OK | CNPJ, valores, razão social |
| 2.2 Enriquecimento | OK | Join por REG_ANS |
| 2.3 Agregação | OK | Total, média, desvio padrão |
| 3.2 DDL | OK | PostgreSQL |
| 3.3 Import | OK | `\copy` |
| 3.4 Queries | OK | 3 queries analíticas |
| 4.2 API | OK | FastAPI |
| 4.3 Frontend | OK | Vue 3 + Chart.js |
| 4.4 Postman | OK | Coleção incluída |
| **Bônus: Cloud** | OK | Neon + Render + Vercel |

## 🌐 Deploy em Produção

**Acesso:** https://teste-intuitive-care-deploy.vercel.app

### Stack de Deploy

| Camada | Serviço | Tecnologia |
|--------|---------|------------|
| Frontend | **Vercel** | CDN global, deploy automático via GitHub |
| API | **Render** | Container Python, uvicorn |
| Banco | **Neon** | PostgreSQL serverless |

### Arquitetura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel    │────▶│   Render    │────▶│    Neon     │
│  (Frontend) │     │   (API)     │     │ (PostgreSQL)│
│   Vue 3     │     │  FastAPI    │     │   Cloud DB  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Por que essas tecnologias?

| Serviço | Justificativa |
|---------|---------------|
| **Neon** | PostgreSQL managed, tier gratuito generoso, conexão SSL |
| **Render** | Deploy simples de Python, integração GitHub, variáveis de ambiente |
| **Vercel** | Otimizado para Vite/Vue, CDN automático, preview por branch |

## Estrutura do Projeto

```
tst_ans/
├── main.py                 # Pipeline ETL
├── src/                    # Módulos do pipeline
│   ├── downloader.py       # Download da ANS
│   ├── extractor.py        # Extração de ZIPs
│   ├── parser.py           # Parsing de arquivos
│   ├── consolidator.py     # Consolidação
│   ├── enrycher.py         # Enriquecimento
│   ├── validator.py        # Validação
│   └── aggregator.py       # Agregação
├── backend/                # API FastAPI
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
├── frontend/               # Vue 3
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   └── api/
├── sql/                    # Scripts SQL
│   ├── 02_ddl.sql
│   ├── 03_import.sql
│   └── 04_queries.sql
├── postman/                # Coleção Postman
└── data/                   # Dados (gerados)
    ├── raw/
    ├── extracted/
    └── output/
```

## Observações

- O CNPJ não está presente nos demonstrativos; o enriquecimento usa `REG_ANS` como chave.
- O pipeline baixa automaticamente os 3 últimos trimestres disponíveis.
- Os caminhos de importação SQL assumem CSVs em `data/output/`.
