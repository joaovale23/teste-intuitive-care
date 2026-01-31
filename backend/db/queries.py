CRESCIMENTO_PERCENTUAL = """
WITH despesas_trimestre AS (
    SELECT
        registro_ans,
        ano,
        trimestre,
        SUM(valor_despesas) AS total
    FROM despesas_consolidadas
    GROUP BY registro_ans, ano, trimestre
),
ordenado AS (
    SELECT
        registro_ans,
        total,
        ROW_NUMBER() OVER (
            PARTITION BY registro_ans
            ORDER BY ano, trimestre
        ) AS rn_asc,
        ROW_NUMBER() OVER (
            PARTITION BY registro_ans
            ORDER BY ano DESC, trimestre DESC
        ) AS rn_desc
    FROM despesas_trimestre
),
primeiro_ultimo AS (
    SELECT
        registro_ans,
        MAX(CASE WHEN rn_asc = 1 THEN total END) AS primeiro_valor,
        MAX(CASE WHEN rn_desc = 1 THEN total END) AS ultimo_valor
    FROM ordenado
    GROUP BY registro_ans
)
SELECT
    o.razao_social,
    ((pu.ultimo_valor - pu.primeiro_valor) / pu.primeiro_valor) * 100
        AS crescimento_percentual
FROM primeiro_ultimo pu
JOIN operadoras o ON o.registro_ans = pu.registro_ans
WHERE pu.primeiro_valor > 0
ORDER BY crescimento_percentual DESC
LIMIT 5;
"""

DESPESAS_TOTAIS="""
SELECT
    uf,
    COUNT(DISTINCT registro_ans) AS total_operadoras,
    SUM(valor_despesas) AS total_despesas,
    ROUND(SUM(valor_despesas) / COUNT(DISTINCT registro_ans)::numeric, 2) AS media_por_operadora,
    ROUND(AVG(valor_despesas), 2) AS media_geral
FROM despesas_agregadas
WHERE uf IS NOT NULL
GROUP BY uf
ORDER BY total_despesas DESC
LIMIT 5;
"""

MEDIA_DESPESAS="""
WITH media_geral AS (
    SELECT AVG(valor_despesas) AS media FROM despesas_consolidadas
),
acima_media AS (
    SELECT
        registro_ans,
        COUNT(*) AS trimestres_acima
    FROM despesas_consolidadas, media_geral
    WHERE valor_despesas > media_geral.media
    GROUP BY registro_ans
)
SELECT COUNT(*) AS operadoras_acima_media
FROM acima_media
WHERE trimestres_acima >= 2;
"""
