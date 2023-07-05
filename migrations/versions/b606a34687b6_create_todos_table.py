"""create_todos_table

Revision ID: b606a34687b6
Revises: 
Create Date: 2023-06-11 14:25:56.124282

"""
from alembic.op import get_bind
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b606a34687b6'
down_revision = None
branch_labels = None
depends_on = None


def exec_raw_sql(query):
    conn = get_bind()
    conn.execute(sa.sql.text(query))


def upgrade() -> None:
    exec_raw_sql(
        """
        CREATE TABLE todos (
            id SERIAL PRIMARY KEY,
            todo VARCHAR NOT NULL,
            due DATE,
            created_at TIMESTAMP DEFAULT NOW()
        );
         """
    )


def downgrade() -> None:
    exec_raw_sql('DROP TABLE todos')
