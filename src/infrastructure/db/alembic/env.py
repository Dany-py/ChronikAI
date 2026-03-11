from logging.config import fileConfig
import os
import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[4]))

import asyncio
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import url
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from src.infrastructure.db.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

load_dotenv()

config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # On récupère la section de config
    conf_section = config.get_section(config.config_ini_section, {})
    
    # On vérifie l'URL dans le fichier .ini ou la config
    url_db = conf_section.get("sqlalchemy.url")

    if url_db and url_db.startswith("sqlite"):
        db_path = url_db.split(":///")[1] if ":///" in url_db else url_db
        if not os.path.isabs(db_path):
            # Résolution par rapport à la racine du projet
            project_root = Path(__file__).resolve().parents[4]
            abs_path = os.path.abspath(project_root / db_path)
            conf_section["sqlalchemy.url"] = f"sqlite+aiosqlite:///{abs_path.replace('\\', '/')}"
            print(f"Base de donnée relative détectée : {url_db}")
            print(f"Base de donnée résolue : {abs_path}")

        print("Running migration in async mode...")
        # Utilisation de la version ASYNC pour créer le moteur
        connectable = async_engine_from_config(
            conf_section,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        asyncio.run(run_async_migrations(connectable))
    else:
        # Mode classique synchrone
        connectable = engine_from_config(
            conf_section,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection, 
                target_metadata=target_metadata,
                render_as_batch=True
            )
            with context.begin_transaction():
                context.run_migrations()

# New asynchronos function
async def run_async_migrations(connectable):
    """Async run migrations in 'online' mode."""
    async with connectable.connect() as connection:
        context.configure(
            connection = connection, target_metadata = target_metadata
        )
        await connection.run_sync(do_run_migrations)
    
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True # Très important pour SQLite
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
