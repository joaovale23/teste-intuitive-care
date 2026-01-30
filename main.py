import pandas as pd

from src.downloader import obter_ultimos_trimestres, baixar_zip
from src.extractor import extrair_zips
from src.parser import processar_pasta
from src.consolidator import consolidar_dados
from src.enrycher import enriquecer_dados
from src.validator import validar_dados
from src.aggregator import agregar_e_exportar as agregar_despesas

PASTA_EXTRAIDA = "data/extracted"
CAMINHO_CONSOLIDADO = "data/output/consolidado_despesas.csv"

def main():
    print("Identificando os últimos trimestres disponíveis...")

    trimestres = obter_ultimos_trimestres(3)

    for ano, trimestre, arquivo in trimestres:
        print(f"Processando {trimestre}T/{ano}")
        baixar_zip(ano, trimestre, arquivo)

    print("Extraindo arquivos ZIP...")
    extrair_zips()

    print("Processando arquivos extraídos...")
    todos_os_dados = []

    for ano, trimestre, _ in trimestres:
        dados = processar_pasta(
            pasta_base=PASTA_EXTRAIDA,
            ano=ano,
            trimestre=trimestre
        )
        todos_os_dados.extend(dados)

    print(f"Registros processados: {len(todos_os_dados)}")
    
    consolidado_despesas = consolidar_dados(todos_os_dados)
    print(f"Arquivo consolidado gerado em: {consolidado_despesas}")

    df_consolidado = pd.read_csv(
        consolidado_despesas,
        sep=";",
        dtype=str
    )

    # Enriquecimento
    print("Enriquecendo dados com cadastro das operadoras...")
    df_enriquecido = enriquecer_dados(df_consolidado)

    # Validação (após enriquecimento, como discutimos)
    print("Validando dados enriquecidos...")
    df_validado = validar_dados(df_enriquecido)

    # Agregação + CSV + ZIP (2.3)
    print("Agregando despesas e gerando arquivo final...")
    agregar_despesas(df_validado)

    print("Pipeline finalizado com sucesso.")

if __name__ == "__main__":
    main()