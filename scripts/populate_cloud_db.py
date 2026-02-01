"""
Script para popular o banco de dados na nuvem.
Uso: python scripts/populate_cloud_db.py

Requer: DATABASE_URL configurada como variável de ambiente
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
import pandas as pd

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERRO: Defina DATABASE_URL com a connection string do Neon")
    print("Exemplo: export DATABASE_URL='postgresql://user:pass@host/db'")
    sys.exit(1)

print(f"Conectando ao banco...")
engine = create_engine(DATABASE_URL)

# DDL - Criar tabelas
DDL = """
-- Tabela: operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans              VARCHAR(20) PRIMARY KEY,
    cnpj                      VARCHAR(20) NOT NULL,
    razao_social              VARCHAR(255) NOT NULL,
    nome_fantasia             VARCHAR(255),
    modalidade                VARCHAR(100),
    logradouro                VARCHAR(255),
    numero                    VARCHAR(20),
    complemento               VARCHAR(255),
    bairro                    VARCHAR(100),
    cidade                    VARCHAR(100),
    uf                        CHAR(2),
    cep                       VARCHAR(10),
    ddd                       VARCHAR(5),
    telefone                  VARCHAR(20),
    fax                       VARCHAR(20),
    endereco_eletronico       VARCHAR(255),
    representante             VARCHAR(255),
    cargo_representante       VARCHAR(255),
    regiao_comercializacao    VARCHAR(100),
    data_registro_ans         DATE
);

-- Tabela: despesas_consolidadas
CREATE TABLE IF NOT EXISTS despesas_consolidadas (
    id                SERIAL PRIMARY KEY,
    cnpj              VARCHAR(20),
    razao_social      VARCHAR(255),
    registro_ans      VARCHAR(20),
    trimestre         INTEGER NOT NULL,
    ano               INTEGER NOT NULL,
    valor_despesas    NUMERIC(18,2) NOT NULL
);

-- Tabela: despesas_agregadas
CREATE TABLE IF NOT EXISTS despesas_agregadas (
    id                SERIAL PRIMARY KEY,
    cnpj              VARCHAR(20) NOT NULL,
    razao_social      VARCHAR(255) NOT NULL,
    registro_ans      VARCHAR(20) NOT NULL,
    modalidade        VARCHAR(100),
    uf                CHAR(2) NOT NULL,
    trimestre         INTEGER NOT NULL,
    ano               INTEGER NOT NULL,
    valor_despesas    NUMERIC(18,2) NOT NULL,
    media_trimestral  NUMERIC(18,2),
    desvio_padrao     NUMERIC(18,2)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_operadoras_uf ON operadoras (uf);
CREATE INDEX IF NOT EXISTS idx_operadoras_cnpj ON operadoras (cnpj);
CREATE INDEX IF NOT EXISTS idx_despesas_periodo ON despesas_consolidadas (ano, trimestre);
CREATE INDEX IF NOT EXISTS idx_despesas_registro_ans ON despesas_consolidadas (registro_ans);
CREATE INDEX IF NOT EXISTS idx_agregadas_uf ON despesas_agregadas (uf);
"""

print("Criando tabelas...")
with engine.connect() as conn:
    for statement in DDL.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))
    conn.commit()
print("Tabelas criadas!")

# Limpar tabelas antes de inserir (para permitir re-execução)
print("Limpando tabelas existentes...")
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE despesas_agregadas, despesas_consolidadas, operadoras CASCADE"))
    conn.commit()
print("Tabelas limpas!")

# Importar dados
DATA_DIR = "data/output"

def importar_csv(tabela, arquivo, mapeamento_colunas):
    """
    Importa CSV para o banco, mapeando nomes de colunas.
    mapeamento_colunas: dict {nome_csv: nome_banco}
    """
    caminho = os.path.join(DATA_DIR, arquivo)
    if not os.path.exists(caminho):
        print(f"  AVISO: {arquivo} não encontrado, pulando...")
        return
    
    print(f"  Importando {arquivo}...")
    df = pd.read_csv(caminho, sep=";", encoding="utf-8", dtype=str)
    
    # Renomear colunas do CSV para nomes do banco
    df = df.rename(columns=mapeamento_colunas)
    
    # Filtrar apenas colunas que existem no mapeamento (valores)
    colunas_banco = list(mapeamento_colunas.values())
    colunas_existentes = [c for c in colunas_banco if c in df.columns]
    df = df[colunas_existentes]
    
    # Remover linhas completamente vazias
    df = df.dropna(how='all')
    
    # Inserir no banco
    df.to_sql(tabela, engine, if_exists="append", index=False)
    print(f"    {len(df)} registros inseridos")

print("\nImportando dados...")

# Operadoras - mapeamento CSV -> Banco
importar_csv(
    "operadoras",
    "operadoras_ativas.csv",
    {
        "REGISTRO_OPERADORA": "registro_ans",
        "CNPJ": "cnpj",
        "Razao_Social": "razao_social",
        "Nome_Fantasia": "nome_fantasia",
        "Modalidade": "modalidade",
        "Logradouro": "logradouro",
        "Numero": "numero",
        "Complemento": "complemento",
        "Bairro": "bairro",
        "Cidade": "cidade",
        "UF": "uf",
        "CEP": "cep",
        "DDD": "ddd",
        "Telefone": "telefone",
        "Fax": "fax",
        "Endereco_eletronico": "endereco_eletronico",
        "Representante": "representante",
        "Cargo_Representante": "cargo_representante",
        "Regiao_de_Comercializacao": "regiao_comercializacao",
        "Data_Registro_ANS": "data_registro_ans"
    }
)

# Despesas consolidadas - mapeamento CSV -> Banco
importar_csv(
    "despesas_consolidadas",
    "consolidado_despesas.csv",
    {
        "CNPJ": "cnpj",
        "RazaoSocial": "razao_social",
        "REG_ANS": "registro_ans",
        "Trimestre": "trimestre",
        "Ano": "ano",
        "ValorDespesas": "valor_despesas"
    }
)

# Despesas agregadas - mapeamento CSV -> Banco
importar_csv(
    "despesas_agregadas",
    "despesas_agregadas.csv",
    {
        "CNPJ": "cnpj",
        "RazaoSocial": "razao_social",
        "RegistroANS": "registro_ans",
        "Modalidade": "modalidade",
        "UF": "uf",
        "Trimestre": "trimestre",
        "Ano": "ano",
        "ValorDespesas": "valor_despesas",
        "MediaTrimestral": "media_trimestral",
        "DesvPadrao": "desvio_padrao"
    }
)

print("\n✓ Banco populado com sucesso!")
