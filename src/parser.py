import pandas as pd
import os

DESCRICAO_FILTRO = "Despesas com Eventos / Sinistros"


def ler_arquivo(caminho: str):
    """
    Lê arquivos CSV/TXT ou XLSX e retorna um DataFrame.
    """
    try:
        if caminho.lower().endswith((".csv", ".txt")):
            return pd.read_csv(
                caminho,
                sep=";",
                encoding="latin1"
            )

        elif caminho.lower().endswith(".xlsx"):
            return pd.read_excel(caminho)

    except Exception as e:
        print(f"Erro ao ler arquivo {caminho}: {e}")

    return None


def normalizar(df: pd.DataFrame, ano: int, trimestre: str):
    """
    Se o arquivo contém 'Despesas com Eventos / Sinistros',
    inclui TODOS os registros do arquivo no resultado.
    Caso contrário, retorna vazio (arquivo descartado).
    
    TRATAMENTO DE VARIAÇÕES:
    - Verifica presença de colunas obrigatórias (resiliente a estruturas variadas)
    - Se colunas obrigatórias não existem, descarta arquivo inteiro
    - Se existem, processa todos os registros (não apenas a descrição alvo)
    - Converte valores monetários de formato BR (1.000,00) para float
    
    VALORES ZERADOS/NEGATIVOS:
    - Mantém todos (indcluindo zerados e negativos)
    - Consolidador marcará como suspeitos para auditoria
    """
    registros = []

    # Colunas obrigatórias segundo análise real dos arquivos
    # Resiliente: se arquivo não tiver essas colunas, é descartado
    colunas_necessarias = [
        "DESCRICAO",
        "REG_ANS",
        "VL_SALDO_FINAL"
    ]

    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            # Arquivo não serve para o processamento
            return registros

    # Verifica se EXISTE ao menos um registro com a descrição alvo
    # Isso qualifica o arquivo para ser processado integralmente
    tem_descricao_alvo = (df["DESCRICAO"] == DESCRICAO_FILTRO).any()

    if not tem_descricao_alvo:
        # Arquivo não contém despesas com eventos/sinistros, descarta
        return registros

    # Se chegou aqui, processa TODO o arquivo
    # Motivo: Se o arquivo tem "Despesas com Eventos / Sinistros",
    # significa que é relevante e todos os registros são válidos
    for _, row in df.iterrows():
        try:
            valor = float(
                str(row["VL_SALDO_FINAL"])
                .replace(".", "")  # Remove separador de milhares
                .replace(",", ".")  # Converte vírgula decimal para ponto
            )
        except Exception:
            # Valor malformado, pula este registro
            continue

        registros.append({
            "CNPJ": "",               # Não disponível na fonte (API ANS)
            "RazaoSocial": "",        # Não disponível na fonte (API ANS)
            "RegistroANS": str(row["REG_ANS"]).strip(),
            "Ano": ano,
            "Trimestre": trimestre,
            "ValorDespesas": valor
        })

    return registros


def processar_arquivo(caminho: str, ano: int, trimestre: str):
    """
    Orquestra leitura + normalização de um único arquivo.
    """
    df = ler_arquivo(caminho)

    if df is None or df.empty:
        return []

    return normalizar(df, ano, trimestre)


def processar_pasta(pasta_base: str, ano: int, trimestre: str):
    """
    Processa todos os arquivos válidos dentro da pasta específica do trimestre.
    Estrutura esperada: pasta_base/YYYY_QT/ (ex: data/extracted/2025_1T/)
    """
    dados = []

    # Construir caminho específico do trimestre
    # trimestre pode ser int (1,2,3) ou str ('1','2','3')
    trimestre_str = str(trimestre).lstrip('0') or '0'  # Remove zeros à esquerda
    pasta_trimestre = os.path.join(pasta_base, f"{ano}_{trimestre_str}T")

    # Verificar se a pasta existe
    if not os.path.exists(pasta_trimestre):
        print(f"Aviso: Pasta não encontrada: {pasta_trimestre}")
        return dados

    # Processar apenas arquivos nesta pasta específica
    for root, _, files in os.walk(pasta_trimestre):
        for file in files:
            caminho_arquivo = os.path.join(root, file)

            if file.lower().endswith((".csv", ".txt", ".xlsx")):
                dados.extend(
                    processar_arquivo(
                        caminho_arquivo,
                        ano,
                        trimestre
                    )
                )

    return dados