"""Add hospital user relationship

Revision ID: c1ba25da74ed
Revises: e1eabd8d9dce
Create Date: 2026-08-09
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c1ba25da74ed"
down_revision = "e1eabd8d9dce"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("hospitals", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_hospitals_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade():
    with op.batch_alter_table("hospitals", schema=None) as batch_op:

        batch_op.drop_constraint(
            "fk_hospitals_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")