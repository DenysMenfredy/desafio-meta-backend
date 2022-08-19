"""renaming tables

Revision ID: 9c12c44be733
Revises: 884aeeca1e53
Create Date: 2022-08-19 12:48:00.549934

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9c12c44be733'
down_revision = '884aeeca1e53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('basecard')
    op.drop_table('cardhastag')
    op.drop_index('name', table_name='basetag')
    op.drop_table('basetag')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basetag',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'basetag', ['name'], unique=False)
    op.create_table('cardhastag',
    sa.Column('card_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tag_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('card_id', 'tag_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('basecard',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('texto', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('data_criacao', mysql.DATETIME(), nullable=True),
    sa.Column('data_modificacao', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
