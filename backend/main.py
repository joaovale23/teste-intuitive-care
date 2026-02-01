from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_db, SessionLocal
from fastapi import Depends
from sqlalchemy import text
from backend.routes.operadoras import router as operadoras_router
from backend.models import Operadora
from backend.db.queries import (
    CRESCIMENTO_PERCENTUAL,
    DESPESAS_TOTAIS,
    MEDIA_DESPESAS,
    TOTAL_MEDIA_DESPESAS,
    TOP_5_OPERADORAS,
)
from src.utils import get_cache, set_cache

app = FastAPI(
    title="API Operadoras ANS",
    description="API para consulta de operadoras e despesas",
    version="1.0.0"
)

# Incluir routers
app.include_router(operadoras_router)

# CORS (necessário para o Vue depois)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção seria restrito
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/api/teste")
def rota_teste():
    return {"mensagem": "API rodando com sucesso"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/db-check")
def db_check(db=Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db_status": result}

@app.get("/api/operadoras-count")
def contar_operadoras(db=Depends(get_db)):
    return {"total": db.query(Operadora).count()}

@app.get("/api/estatisticas")
def estatisticas(db=Depends(get_db)):
    """Retorna estatísticas agregadas das operadoras."""
    cache_key = "estatisticas"

    cached = get_cache(cache_key)
    if cached:
        return {
            "cached": True,
            **cached
        }

    try:
        crescimento = db.execute(text(CRESCIMENTO_PERCENTUAL)).mappings().all()
        despesas_por_uf = db.execute(text(DESPESAS_TOTAIS)).mappings().all()
        media = db.execute(text(MEDIA_DESPESAS)).mappings().one_or_none()
        totais = db.execute(text(TOTAL_MEDIA_DESPESAS)).mappings().one_or_none()
        top_5 = db.execute(text(TOP_5_OPERADORAS)).mappings().all()

        result = {
            "total_despesas": totais["total_despesas"] if totais else 0,
            "media_despesas": totais["media_despesas"] if totais else 0,
            "top_5_operadoras": list(top_5),
            "despesas_por_uf": list(despesas_por_uf),
            "operadoras_acima_media": media["operadoras_acima_media"] if media else 0,
            "top_5_crescimento": list(crescimento),
        }

        set_cache(cache_key, result, ttl=300)  # 5 minutos

        return {
            "cached": False,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular estatísticas: {str(e)}"
        )
