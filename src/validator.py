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
    df = df.copy()

    # Valor positivo
    df["ValorDespesas"] = pd.to_numeric(
        df["ValorDespesas"],
        errors="coerce"
    )

    df = df[df["ValorDespesas"] > 0]

    # Razão social válida
    df["RazaoSocial"] = df["RazaoSocial"].astype(str).str.strip()
    df = df[df["RazaoSocial"] != ""]

    # Validação de CNPJ (após enriquecimento, CNPJ vem do cadastro)
    df["cnpj_valido"] = df["CNPJ"].apply(validar_cnpj)
    print(f"CNPJs inválidos encontrados: {(~df['cnpj_valido']).sum()}")
    
    # Descartar registros com CNPJ inválido
    df = df[df["cnpj_valido"]]

    return df
