from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 declarative base for all models."""
    pass


# ---------------------------------------------------------------------------
# Import every model module here so Alembic's autogenerate sees all tables.
# ---------------------------------------------------------------------------
def import_all_models() -> None:
    """Force-import all model modules to register them with Base.metadata."""
    import app.modules.auth.models  # noqa: F401
    import app.modules.materials.models  # noqa: F401
    import app.modules.inventory.models  # noqa: F401
    import app.modules.products.models  # noqa: F401
    import app.modules.production.models  # noqa: F401
    import app.modules.sales.models  # noqa: F401
