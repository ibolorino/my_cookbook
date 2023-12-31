"""Add Ingredient model

Revision ID: 43ee2baaa050
Revises: ef4635ecaf39
Create Date: 2023-06-19 03:35:20.028119

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "43ee2baaa050"
down_revision = "ef4635ecaf39"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredient",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("quantity", sa.String(), nullable=True),
        sa.Column("recipe_item_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["recipe_item_id"],
            ["recipeitem.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingredient_id"), "ingredient", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_ingredient_id"), table_name="ingredient")
    op.drop_table("ingredient")
    # ### end Alembic commands ###
