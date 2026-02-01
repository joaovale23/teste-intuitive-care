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
    """Pipeline ETL para dados da ANS."""
    try:
        print("="*60)
        print("PIPELINE ETL - DEMONSTRAÇÕES CONTÁBEIS ANS")
        print("="*60)
        
        print("\n[1/6] Identificando os últimos trimestres disponíveis...")
        trimestres = obter_ultimos_trimestres(3)
        
        if not trimestres:
            print("ERRO: Nenhum trimestre encontrado na fonte de dados.")
            return
        
        print(f"      Trimestres encontrados: {[(t[1], t[0]) for t in trimestres]}")

        print("\n[2/6] Baixando arquivos ZIP...")
        for ano, trimestre, arquivo in trimestres:
            print(f"      → {trimestre}T/{ano}")
            baixar_zip(ano, trimestre, arquivo)

        print("\n[3/6] Extraindo arquivos ZIP...")
        extrair_zips()

        print("\n[4/6] Processando arquivos extraídos...")
        todos_os_dados = []

        for ano, trimestre, _ in trimestres:
            dados = processar_pasta(
                pasta_base=PASTA_EXTRAIDA,
                ano=ano,
                trimestre=trimestre
            )
            todos_os_dados.extend(dados)
            print(f"      → {trimestre}T/{ano}: {len(dados)} registros")

        print(f"\n      Total de registros processados: {len(todos_os_dados)}")
        
        if not todos_os_dados:
            print("ERRO: Nenhum registro extraído dos arquivos.")
            return
        
        consolidado_despesas = consolidar_dados(todos_os_dados)
        
        if not consolidado_despesas:
            print("ERRO: Falha ao gerar arquivo consolidado.")
            return
            
        print(f"      Arquivo consolidado: {consolidado_despesas}")

        df_consolidado = pd.read_csv(
            consolidado_despesas,
            sep=";",
            dtype=str
        )

        print("\n[5/6] Enriquecendo dados com cadastro das operadoras...")
        df_enriquecido = enriquecer_dados(df_consolidado)
        print(f"      Registros após enriquecimento: {len(df_enriquecido)}")

        print("\n[6/6] Validando e agregando dados...")
        df_validado = validar_dados(df_enriquecido)
        print(f"      Registros válidos: {len(df_validado)}")
        
        if df_validado.empty:
            print("ERRO: Nenhum registro válido após validação.")
            return

        agregar_despesas(df_validado)

        print("\n" + "="*60)
        print("PIPELINE FINALIZADO COM SUCESSO!")
        print("="*60)
        
    except Exception as e:
        print(f"\nERRO FATAL: {e}")
        raise

if __name__ == "__main__":
    main()