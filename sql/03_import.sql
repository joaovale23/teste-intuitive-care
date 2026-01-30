-- Executar este script via:
-- psql -U postgres -d tst_ans -f sql/03_import.sql


-- ===============================
-- IMPORTAÇÃO: despesas consolidadas
-- ===============================
\copy despesas_consolidadas (cnpj, razao_social, registro_ans, trimestre, ano, valor_despesas) FROM 'data/output/consolidado_despesas.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';


-- ===============================
-- IMPORTAÇÃO: operadoras
-- ===============================
\copy operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_comercializacao, data_registro_ans) FROM 'data/output/operadoras_ativas.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';


-- ===============================
-- IMPORTAÇÃO: despesas agregadas
-- ===============================
\copy despesas_agregadas (cnpj, razao_social, trimestre, ano, valor_despesas, media_trimestral, desvio_padrao, registro_ans, modalidade, uf) FROM 'data/output/despesas_agregadas.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8';
