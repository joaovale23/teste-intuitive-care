from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

class OperadoraBase(BaseModel):
    registro_ans: str
    cnpj: str
    razao_social: str
    uf: Optional[str]

    class Config:
        from_attributes = True

class OperadoraDetalhe(BaseModel):
    registro_ans: str
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str]
    modalidade: Optional[str]
    logradouro: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]
    cep: Optional[str]
    telefone: Optional[str]
    endereco_eletronico: Optional[str]
    representante: Optional[str]
    cargo_representante: Optional[str]
    regiao_comercializacao: Optional[str]
    data_registro_ans: Optional[date]

    class Config:
        from_attributes = True

class DespesaOperadora(BaseModel):
    ano: int
    trimestre: int
    valor_despesas: Decimal

    class Config:
        from_attributes = True

class EstatisticasResponse(BaseModel):
    total_despesas: Decimal
    media_despesas: Decimal
    top_5_operadoras: List[OperadoraBase]

class PaginatedResponse(BaseModel):
    data: list
    total: int
    page: int
    limit: int
