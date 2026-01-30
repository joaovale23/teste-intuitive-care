import pandas as pd
from src.downloader import baixar_cadastro_operadoras


def enriquecer_dados(df_despesas: pd.DataFrame) -> pd.DataFrame:
    caminho = baixar_cadastro_operadoras()

    df_cadastro = pd.read_csv(
        caminho,
        sep=";",
        dtype=str,
        encoding="latin1"
    )

    df_cadastro.columns = [c.lower() for c in df_cadastro.columns]

    # Mapeamento resiliente de colunas
    mapa_colunas = {}
    
    for col in df_cadastro.columns:
        if col == "registro_operadora":
            mapa_colunas[col] = "registro_operadora"
        elif col == "cnpj":
            mapa_colunas[col] = "cnpj"
        elif col == "modalidade":
            mapa_colunas[col] = "modalidade"
        elif col == "uf":
            mapa_colunas[col] = "uf"

    df_cadastro = df_cadastro.rename(columns=mapa_colunas)

    # Limpar aspas dos valores (formato CSV do cadastro)
    for col in ["cnpj", "registro_operadora", "modalidade", "uf"]:
        if col in df_cadastro.columns:
            df_cadastro[col] = df_cadastro[col].str.strip('"')

    # Drop duplicates apenas se a coluna existir
    if "registro_operadora" in df_cadastro.columns:
        df_cadastro = df_cadastro.drop_duplicates(
            subset="registro_operadora",
            keep="first"
        )

    # Merge com a coluna correta
    if "registro_operadora" in df_cadastro.columns:
        df_final = df_despesas.merge(
            df_cadastro,
            left_on="REG_ANS",
            right_on="registro_operadora",
            how="inner"  # Estratégia: manter apenas registros que encontram match no cadastro
        )
        
        registros_sem_match = len(df_despesas) - len(df_final)
        if registros_sem_match > 0:
            print(f"⚠️ {registros_sem_match} registros descartados por não encontrar match no cadastro")
        
        # Drop das colunas vazias do consolidado e renomear as do cadastro
        if "CNPJ" in df_final.columns and "cnpj" in df_final.columns:
            df_final = df_final.drop(columns=["CNPJ"])
            df_final = df_final.rename(columns={"cnpj": "CNPJ"})
        
        if "RazaoSocial" in df_final.columns and "razao_social" in df_final.columns:
            df_final = df_final.drop(columns=["RazaoSocial"])
            df_final = df_final.rename(columns={"razao_social": "RazaoSocial"})
    else:
        print("Aviso: Coluna 'registro_operadora' não encontrada no cadastro. Retornando dados sem enriquecimento.")
        df_final = df_despesas

    return df_final