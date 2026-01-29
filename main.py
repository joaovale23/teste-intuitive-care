from src.downloader import obter_ultimos_trimestres, baixar_zip
from src.extractor import extrair_zips
from src.parser import processar_pasta
from src.consolidator import consolidar_dados

PASTA_EXTRAIDA = "data/extracted"

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

    print(f"Arquivo final gerado em: {consolidado_despesas}")


if __name__ == "__main__":
    main()