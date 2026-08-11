"""Add medicine active status

Revision ID: a17fd6a332e9
Revises: 99a2722c9a7f
Create Date: 2026-08-09
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a17fd6a332e9"
down_revision = "99a2722c9a7f"
branch_labels = None
depends_on = None


def upgrade():
    # SQLite uses a temporary table when altering an existing table.
    # The previous migration attempt failed and left that temporary
    # table behind, so remove it before retrying.

    op.execute(
        "DROP TABLE IF EXISTS _alembic_tmp_medicines"
    )

    with op.batch_alter_table(
        "medicines",
        schema=None
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )


def downgrade():

    # Remove any leftover temporary table
    # before performing the downgrade.
    op.execute(
        "DROP TABLE IF EXISTS _alembic_tmp_medicines"
    )

    with op.batch_alter_table(
        "medicines",
        schema=None
    ) as batch_op:

        batch_op.drop_column("is_active")