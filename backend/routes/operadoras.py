from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, asc

from backend.database import get_db
from backend.models import Operadora
from backend.models import DespesaConsolidada

router = APIRouter(prefix="/api/operadoras", tags=["Operadoras"])


@router.get("")
def listar_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    total = db.execute(
        text("SELECT COUNT(*) FROM operadoras")
    ).scalar()

    operadoras = db.execute(
        text("""
            SELECT
                registro_ans,
                cnpj,
                razao_social,
                nome_fantasia,
                modalidade,
                uf
            FROM operadoras
            ORDER BY razao_social
            LIMIT :limit OFFSET :offset
        """),
        {
            "limit": limit,
            "offset": offset
        }
    ).mappings().all()

    return {
        "data": list(operadoras),
        "page": page,
        "limit": limit,
        "total": total
    }

@router.get("/{cnpj}")
def detalhar_operadora(
    cnpj: str,
    db: Session = Depends(get_db)
):
    operadora = (
        db.query(Operadora)
        .filter(Operadora.cnpj == cnpj)
        .first()
    )

    if not operadora:
        raise HTTPException(
            status_code=404,
            detail="Operadora não encontrada"
        )

    return operadora

@router.get("/{cnpj}/despesas")
def despesas_da_operadora(
    cnpj: str,
    db: Session = Depends(get_db)
):
    operadora = (
        db.query(Operadora)
        .filter(Operadora.cnpj == cnpj)
        .first()
    )

    if not operadora:
        raise HTTPException(
            status_code=404,
            detail="Operadora não encontrada"
        )

    despesas = (
        db.query(
            DespesaConsolidada.ano,
            DespesaConsolidada.trimestre,
            DespesaConsolidada.valor_despesas
        )
        .filter(DespesaConsolidada.registro_ans == operadora.registro_ans)
        .order_by(
            asc(DespesaConsolidada.ano),
            asc(DespesaConsolidada.trimestre)
        )
        .all()
    )

    return {
        "cnpj": cnpj,
        "razao_social": operadora.razao_social,
        "registro_ans": operadora.registro_ans,
        "modalidade": operadora.modalidade,
        "uf": operadora.uf,
        "cidade": operadora.cidade,
        "historico": [{"ano": d[0], "trimestre": d[1], "valor_despesas": d[2]} for d in despesas] if despesas else []
    }


@router.get("/estatisticas/despesas-uf")
def despesas_por_uf(db: Session = Depends(get_db)):
    """Retorna despesas agregadas por UF para o gráfico"""
    despesas = db.execute(
        text("""
            SELECT uf, SUM(CAST(valor_despesas AS FLOAT)) as total
            FROM despesas_agregadas
            GROUP BY uf
            ORDER BY uf
        """)
    ).fetchall()
    
    return {
        "labels": [d[0] for d in despesas],
        "values": [float(d[1]) if d[1] else 0 for d in despesas],
        "data": [
            {
                "uf": d[0],
                "valor_despesas": float(d[1]) if d[1] else 0
            }
            for d in despesas
        ]
    }
