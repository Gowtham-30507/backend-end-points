from collections.abc import Generator
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.config import settings

logger = logging.getLogger(__name__)

# Determine if SQLite or PostgreSQL/other dialect
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create SQLAlchemy 2.x Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative Base for ORM models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session and ensuring safe cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> dict[str, str]:
    """
    Verify database connectivity safely without crashing the application.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "connected", "database": "accessible"}
    except Exception as exc:
        logger.warning("Database connectivity check failed: %s", exc)
        return {"status": "unavailable", "detail": str(exc)}
