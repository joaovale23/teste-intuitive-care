import pandas as pd
import zipfile
from pathlib import Path


def agregar_e_exportar(
    df: pd.DataFrame,
    output_dir: str = "data/output"
) -> None:
    """
    Agrega despesas por CNPJ, RazaoSocial, Trimestre, Ano e UF.
    Mantém as 5 colunas do consolidado + 3 do enriquecimento (RegistroANS, Modalidade, UF).
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / "despesas_agregadas.csv"
    zip_path = output_path / "Teste_Joao_Vitor_Vale_da_Cruz.zip"

    # Garante tipo numérico
    df["ValorDespesas"] = pd.to_numeric(
        df["ValorDespesas"],
        errors="coerce"
    )

    # Renomear colunas para o padrão correto
    df = df.rename(columns={
        "registro_operadora": "RegistroANS",
        "uf": "UF"
    })

    # Agregação por RazaoSocial e UF conforme requisito 2.3
    # Calcula total, média e desvio padrão de despesas por operadora/UF
    df_agregado = (
        df
        .groupby(["RazaoSocial", "UF"], as_index=False)
        .agg(
            CNPJ=("CNPJ", "first"),                          # Pega primeiro CNPJ
            Trimestre=("Trimestre", "first"),                # Pega primeiro trimestre
            Ano=("Ano", "first"),                            # Pega primeiro ano
            ValorDespesas=("ValorDespesas", "sum"),          # SOMA de despesas
            MediaTrimestral=("ValorDespesas", "mean"),       # Média por trimestre
            DesvPadrao=("ValorDespesas", "std"),             # Desvio padrão
            RegistroANS=("RegistroANS", "first"),            # Único por operadora
            Modalidade=("modalidade", "first")               # Único por operadora
        )
        # Ordenar por valor total (maior para menor)
        .sort_values(by="ValorDespesas", ascending=False)
    )

    # Reordenar colunas no padrão especificado
    colunas_finais = ["CNPJ", "RazaoSocial", "Trimestre", "Ano", "ValorDespesas", "MediaTrimestral", "DesvPadrao", "RegistroANS", "Modalidade", "UF"]
    df_agregado = df_agregado[colunas_finais]

    # Salva CSV
    df_agregado.to_csv(
        csv_path,
        index=False,
        sep=";"
    )

    # Compacta em ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, arcname=csv_path.name)

    print(f"CSV agregado salvo em: {csv_path}")
    print(f"Arquivo ZIP gerado em: {zip_path}")
