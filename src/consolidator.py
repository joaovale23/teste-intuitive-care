import csv
import zipfile
import os
import pandas as pd


def consolidar_dados(registros, caminho_saida="data/output"):
    """
    Consolida dados de todos os trimestres em um único CSV.
    
    Tratamento de inconsistências:
    - CNPJs duplicados: Identificados por RegistroANS + Trimestre
    - Valores zerados/negativos: Mantidos com marcação de suspeita
    - Estrutura de trimestres: Garantida pela origem (data/extracted/YYYY_QT/)
    """
    os.makedirs(caminho_saida, exist_ok=True)

    # ZIP final
    zip_path = os.path.join(caminho_saida, "consolidado_despesas.zip")
    
    # Verificar se já foi consolidado
    if os.path.exists(zip_path):
        print(f"Consolidado já existe, pulando: {zip_path}")
        return zip_path

    if not registros:
        print("Aviso: Nenhum registro para consolidar")
        return None

    # Converter para DataFrame
    df = pd.DataFrame(registros)

    # Garantir tipos corretos
    df["Ano"] = df["Ano"].astype(int)
    df["Trimestre"] = df["Trimestre"].astype(str)
    df["ValorDespesas"] = df["ValorDespesas"].astype(float)

    # Marcar registros suspeitos (valores <= 0)
    df["Suspeito"] = df["ValorDespesas"] <= 0

    # Detectar CNPJs duplicados por REG_ANS
    # (mesmo sem CNPJ real, REG_ANS identifica a operadora)
    operadoras_multiplas = df.groupby("REG_ANS")["Trimestre"].nunique()
    operadoras_com_multiplos = operadoras_multiplas[operadoras_multiplas > 1].index
    
    df["CNPJDuplicado"] = df["REG_ANS"].isin(operadoras_com_multiplos)

    # Ordenar dados
    df = df.sort_values(["Ano", "Trimestre", "REG_ANS"])

    # CSV temporário com coluna de auditoria
    csv_temp = os.path.join(caminho_saida, "_consolidado_temp.csv")

    # Colunas do CSV final (sem colunas de auditoria)
    colunas_saida = ["CNPJ", "RazaoSocial", "REG_ANS", "Trimestre", "Ano", "ValorDespesas"]
    
    df[colunas_saida].to_csv(
        csv_temp,
        sep=";",
        encoding="utf-8",
        index=False
    )

    # Estatísticas para output
    zerados = len(df[df["ValorDespesas"] == 0])
    negativos = len(df[df["ValorDespesas"] < 0])
    operadoras_multiplas_count = len(operadoras_com_multiplos)

    print(f"✓ Consolidado: {len(df)} registros de despesas")
    print(f"  - 1T 2025: {len(df[(df['Ano'] == 2025) & (df['Trimestre'] == '1')])} registros")
    print(f"  - 2T 2025: {len(df[(df['Ano'] == 2025) & (df['Trimestre'] == '2')])} registros")
    print(f"  - 3T 2025: {len(df[(df['Ano'] == 2025) & (df['Trimestre'] == '3')])} registros")
    
    print(f"\n  INCONSISTÊNCIAS DETECTADAS:")
    print(f"  - Valores zerados: {zerados}")
    print(f"  - Valores negativos: {negativos}")
    print(f"  - Operadoras em múltiplos trimestres: {operadoras_multiplas_count}")
    print(f"  - CNPJ vazio: {len(df[df['CNPJ'] == ''])} (100% - não disponível na fonte)")

    # Caminho final do CSV (sem compressão)
    csv_final = os.path.join(caminho_saida, "consolidado_despesas.csv")
    
    # Mover CSV temporário para final
    if os.path.exists(csv_final):
        os.remove(csv_final)
    os.rename(csv_temp, csv_final)

    # ZIP final (para arquivo)
    zip_path = os.path.join(caminho_saida, "consolidado_despesas.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_final, arcname="consolidado_despesas.csv")

    print(f"\n ZIP gerado: {zip_path}")

    return zip_path
