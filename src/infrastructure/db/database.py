# db/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL is not set")

# Résolution du chemin relatif pour SQLite
if "sqlite" in db_url:
    if ":///" in db_url:
        protocol, path = db_url.split(":///", 1)
        if not os.path.isabs(path) and not path.startswith("/"):
            # Chemin relatif, on le résout par rapport à la racine du projet
            # On suppose que ce fichier est dans src/infrastructure/db/
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
            abs_path = os.path.abspath(os.path.join(project_root, path))
            db_url = f"{protocol}:///{abs_path.replace('\\', '/')}"
            print(f"Base de donnée résolue : {db_url}")

engine = create_async_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False}  # important pour SQLite
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()