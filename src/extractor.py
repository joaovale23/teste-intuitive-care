import os
import zipfile
import re

RAW_DIR = "data/raw"
EXTRACTED_DIR = "data/extracted"


def criar_diretorio(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def extrair_zips():
    criar_diretorio(EXTRACTED_DIR)

    for arquivo in os.listdir(RAW_DIR):
        if not arquivo.lower().endswith(".zip"):
            continue

        # Exemplo de nome: 2025_3T_3T2025.zip
        match = re.match(r"(\d{4})_(\d)T_", arquivo)

        if not match:
            print(f"Nome inesperado, ignorando: {arquivo}")
            continue

        ano = match.group(1)
        trimestre = match.group(2)

        destino = os.path.join(EXTRACTED_DIR, f"{ano}_{trimestre}T")
        criar_diretorio(destino)

        if os.listdir(destino):
            print(f"Já extraído, pulando: {destino}")
            continue

        caminho_zip = os.path.join(RAW_DIR, arquivo)

        print(f"Extraindo {arquivo} → {destino}")

        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            zip_ref.extractall(destino)