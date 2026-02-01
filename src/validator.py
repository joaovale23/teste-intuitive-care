import pandas as pd
import re


def validar_cnpj(cnpj: str) -> bool:
    if not isinstance(cnpj, str):
        return False

    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, peso):
        soma = sum(int(cnpj[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [6] + peso1

    digito1 = calcular_digito(cnpj[:12], peso1)
    digito2 = calcular_digito(cnpj[:13], peso2)

    return cnpj[-2:] == digito1 + digito2


def validar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida e limpa os dados enriquecidos.
    
    Validações aplicadas:
    - ValorDespesas > 0 (valores zerados/negativos removidos)
    - RazaoSocial não vazia
    - CNPJ válido (formato e dígitos verificadores)
    
    Args:
        df: DataFrame com dados enriquecidos.
        
    Returns:
        DataFrame apenas com registros válidos.
    """
    df = df.copy()
    total_inicial = len(df)

    # Converter valor para numérico
    df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce")
    
    # Filtrar valores positivos
    df = df[df["ValorDespesas"] > 0]
    removidos_valor = total_inicial - len(df)

    # Razão social válida
    df["RazaoSocial"] = df["RazaoSocial"].astype(str).str.strip()
    antes_razao = len(df)
    df = df[df["RazaoSocial"] != ""]
    removidos_razao = antes_razao - len(df)

    # Validação de CNPJ
    df["cnpj_valido"] = df["CNPJ"].apply(validar_cnpj)
    cnpjs_invalidos = (~df["cnpj_valido"]).sum()
    df = df[df["cnpj_valido"]]
    
    # Remover coluna auxiliar
    df = df.drop(columns=["cnpj_valido"], errors="ignore")

    # Log de validação
    print(f"      Removidos por valor <= 0: {removidos_valor}")
    print(f"      Removidos por razão social vazia: {removidos_razao}")
    print(f"      Removidos por CNPJ inválido: {cnpjs_invalidos}")

    return df
