"""Создание таблицы заметок."""

from alembic import op


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE notes (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL DEFAULT 1,
            title VARCHAR(80) NOT NULL
                CHECK (char_length(title) >= 1),
            content VARCHAR(500) NOT NULL
                CHECK (char_length(content) >= 1)
        );
    """)


def downgrade():
    op.drop_table("notes")