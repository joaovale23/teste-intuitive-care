from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("AVISO: DATABASE_URL não definida, usando conexão local", file=sys.stderr)
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/tst_ans"
else:
    # Render/Neon usam 'postgres://' mas SQLAlchemy requer 'postgresql://'
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"DATABASE_URL configurada: {DATABASE_URL[:30]}...", file=sys.stderr)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
