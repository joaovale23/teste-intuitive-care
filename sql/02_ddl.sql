-- ============================================
-- 01_ddl.sql
-- Estrutura de tabelas - Teste Intuitive Care
-- Banco: PostgreSQL
-- ============================================


-- =========================
-- TABELA: despesas_consolidadas
-- Dados trimestrais
-- =========================
CREATE TABLE despesas_consolidadas (
    id                SERIAL PRIMARY KEY,
    cnpj              VARCHAR(20),
    razao_social      VARCHAR(255),
    registro_ans      VARCHAR(20),
    trimestre         INTEGER NOT NULL,
    ano               INTEGER NOT NULL,
    valor_despesas    NUMERIC(18,2) NOT NULL
);

CREATE INDEX idx_despesas_periodo
    ON despesas_consolidadas (ano, trimestre);

CREATE INDEX idx_despesas_registro_ans
    ON despesas_consolidadas (registro_ans);


-- =========================
-- TABELA: operadoras
-- Dados cadastrais
-- =========================
CREATE TABLE operadoras (
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

CREATE INDEX idx_operadoras_uf
    ON operadoras (uf);

CREATE INDEX idx_operadoras_cnpj
    ON operadoras (cnpj);


-- =========================
-- TABELA: despesas_agregadas
-- Resultado analítico
-- =========================
CREATE TABLE despesas_agregadas (
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

CREATE INDEX idx_agregadas_uf
    ON despesas_agregadas (uf);

CREATE INDEX idx_agregadas_periodo
    ON despesas_agregadas (ano, trimestre);
