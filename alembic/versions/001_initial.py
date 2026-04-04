"""Initial migration — all tables

Revision ID: 001_initial
Revises:
Create Date: 2026-04-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False, index=True),
        sa.Column("email", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("admin", "production", "finance", name="userrole"), nullable=False, server_default="admin"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Refresh Tokens ---
    op.create_table(
        "refresh_tokens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(512), unique=True, nullable=False, index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Units ---
    op.create_table(
        "units",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=False),
    )

    # --- Raw Materials ---
    op.create_table(
        "raw_materials",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, index=True),
        sa.Column("primary_unit_id", UUID(as_uuid=True), sa.ForeignKey("units.id"), nullable=False),
        sa.Column("secondary_unit_id", UUID(as_uuid=True), sa.ForeignKey("units.id"), nullable=False),
        sa.Column("conversion_factor", sa.Float(), nullable=False),
        sa.Column("stock_primary", sa.Float(), server_default="0"),
        sa.Column("stock_secondary", sa.Float(), server_default="0"),
        sa.Column("cost_cpp", sa.Float(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Inventory Movements ---
    op.create_table(
        "inventory_movements",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("material_id", UUID(as_uuid=True), sa.ForeignKey("raw_materials.id"), nullable=False),
        sa.Column("type", sa.Enum("IN", "OUT", name="movementtype"), nullable=False),
        sa.Column("quantity_primary", sa.Float(), nullable=False),
        sa.Column("quantity_secondary", sa.Float(), nullable=False),
        sa.Column("unit_cost", sa.Float(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Products ---
    op.create_table(
        "products",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, index=True),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- BOM Items ---
    op.create_table(
        "bom_items",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("material_id", UUID(as_uuid=True), sa.ForeignKey("raw_materials.id"), nullable=False),
        sa.Column("quantity_required", sa.Float(), nullable=False),
    )

    # --- Production Orders ---
    op.create_table(
        "production_orders",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum("pending", "in_progress", "completed", name="orderstatus"), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # --- Production Consumptions ---
    op.create_table(
        "production_consumptions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("production_order_id", UUID(as_uuid=True), sa.ForeignKey("production_orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("material_id", UUID(as_uuid=True), sa.ForeignKey("raw_materials.id"), nullable=False),
        sa.Column("quantity_used", sa.Float(), nullable=False),
    )

    # --- Clients ---
    op.create_table(
        "clients",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=True),
    )

    # --- Sales ---
    op.create_table(
        "sales",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("client_id", UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("sales")
    op.drop_table("clients")
    op.drop_table("production_consumptions")
    op.drop_table("production_orders")
    op.drop_table("bom_items")
    op.drop_table("products")
    op.drop_table("inventory_movements")
    op.drop_table("raw_materials")
    op.drop_table("units")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS movementtype")
    op.execute("DROP TYPE IF EXISTS orderstatus")
