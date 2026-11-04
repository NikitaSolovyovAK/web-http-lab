"""Добавление признака архива для заметок."""

from alembic import op


revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE notes "
        "ADD COLUMN is_archived BOOLEAN NOT NULL DEFAULT FALSE"
    )


def downgrade():
    op.drop_column("notes", "is_archived")