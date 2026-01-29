import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

RAW_DATA_DIR = "data/raw"


def criar_diretorio(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def listar_diretorios(url: str):
    """
    Retorna uma lista de nomes de diretórios disponíveis em uma URL
    """
    response = requests.get(url)
    response.raise_for_status()

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

def baixar_zip(ano: int, trimestre: int, nome_arquivo: str):
    criar_diretorio(RAW_DATA_DIR)

    nome_local = f"{ano}_{trimestre}T_{nome_arquivo}"
    caminho_arquivo = os.path.join(RAW_DATA_DIR, nome_local)

    if os.path.exists(caminho_arquivo):
        print(f"Arquivo já existe, pulando: {nome_local}")
        return

    url_arquivo = urljoin(BASE_URL, f"{ano}/{nome_arquivo}")

    print(f"Baixando: {nome_local}")

    with requests.get(url_arquivo, stream=True) as r:
        r.raise_for_status()
        with open(caminho_arquivo, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)