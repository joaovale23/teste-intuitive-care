import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
URL_CADASTRO_OPERADORAS =  "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"


RAW_DATA_DIR = "data/raw"
PASTA_SAIDA = "data/output"


def criar_diretorio(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def listar_diretorios(url: str):
    """
    Retorna uma lista de nomes de diretórios disponíveis em uma URL.
    
    Args:
        url: URL do diretório FTP/HTTP a listar.
        
    Returns:
        Lista de nomes de diretórios encontrados.
        
    Raises:
        requests.RequestException: Se houver falha na conexão.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    diretorios = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith("/") and href not in ["../"]:
            diretorios.append(href.strip("/"))

    return diretorios

def obter_ultimos_trimestres(qtd: int = 3):
    """
    Retorna uma lista de tuplas:
    (ano, trimestre, nome_arquivo)
    Ex: (2025, 1, '1T2025.zip')
    """
    anos = listar_diretorios(BASE_URL)
    encontrados = []

    for ano in anos:
        if not ano.isdigit() or len(ano) != 4:
            continue

        ano_url = urljoin(BASE_URL, f"{ano}/")
        response = requests.get(ano_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")

            if not href or not href.lower().endswith(".zip"):
                continue

            # Padrão esperado: 1T2025.zip
            match = re.match(r"([1-4])T(\d{4})\.zip", href)

            if match:
                trimestre = int(match.group(1))
                ano_arquivo = int(match.group(2))

                encontrados.append(
                    (ano_arquivo, trimestre, href)
                )

    # Ordena do mais recente para o mais antigo
    encontrados.sort(key=lambda x: (x[0], x[1]), reverse=True)

    return encontrados[:qtd]

def baixar_zip(ano: int, trimestre: int, nome_arquivo: str) -> bool:
    """
    Baixa um arquivo ZIP de demonstrações contábeis.
    
    Args:
        ano: Ano do arquivo.
        trimestre: Trimestre (1-4).
        nome_arquivo: Nome do arquivo ZIP.
        
    Returns:
        True se baixou com sucesso ou já existia, False se falhou.
    """
    criar_diretorio(RAW_DATA_DIR)

    nome_local = f"{ano}_{trimestre}T_{nome_arquivo}"
    caminho_arquivo = os.path.join(RAW_DATA_DIR, nome_local)

    if os.path.exists(caminho_arquivo):
        print(f"        ✓ Já existe: {nome_local}")
        return True

    url_arquivo = urljoin(BASE_URL, f"{ano}/{nome_arquivo}")

    try:
        with requests.get(url_arquivo, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(caminho_arquivo, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"        ✓ Baixado: {nome_local}")
        return True
    except requests.RequestException as e:
        print(f"        ✗ Erro ao baixar {nome_local}: {e}")
        return False

def baixar_cadastro_operadoras():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(PASTA_SAIDA, "operadoras_ativas.csv")

    if os.path.exists(caminho):
        print("Cadastro de operadoras já existe, pulando download.")
        return caminho

    print("⬇️ Baixando cadastro de operadoras ativas...")
    response = requests.get(URL_CADASTRO_OPERADORAS)
    response.raise_for_status()

    with open(caminho, "wb") as f:
        f.write(response.content)

    print("Cadastro salvo em:", caminho)
    return caminho