"""Added relationships and methods

Revision ID: 774f4e06401e
Revises: 10665e093ff8
Create Date: 2025-03-05 18:16:09.379213

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '774f4e06401e'
down_revision = '10665e093ff8'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create new companies table with NOT NULL constraints
    op.create_table(
        'new_companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),  # NOT NULL added
        sa.Column('founding_year', sa.Integer, nullable=False),  # NOT NULL added
    )
    
    # Copy data from old table to new table
    op.execute("INSERT INTO new_companies (id, name, founding_year) SELECT id, name, founding_year FROM companies")
    
    # Drop old table
    op.drop_table('companies')
    
    # Rename new table to original name
    op.rename_table('new_companies', 'companies')

    # Create new devs table with NOT NULL constraints
    op.create_table(
        'new_devs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),  # NOT NULL added
    )
    
    # Copy data from old table to new table
    op.execute("INSERT INTO new_devs (id, name) SELECT id, name FROM devs")
    
    # Drop old table
    op.drop_table('devs')
    
    # Rename new table to original name
    op.rename_table('new_devs', 'devs')

def downgrade() -> None:
    # Recreate companies table without NOT NULL constraints
    op.create_table(
        'old_companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=True),  # Allow NULL
        sa.Column('founding_year', sa.Integer, nullable=True),  # Allow NULL
    )
    
    # Copy data back to original structure
    op.execute("INSERT INTO old_companies (id, name, founding_year) SELECT id, name, founding_year FROM companies")
    
    # Drop modified table
    op.drop_table('companies')
    
    # Rename back to original
    op.rename_table('old_companies', 'companies')

    # Recreate devs table without NOT NULL constraints
    op.create_table(
        'old_devs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=True),  # Allow NULL
    )
    
    # Copy data back to original structure
    op.execute("INSERT INTO old_devs (id, name) SELECT id, name FROM devs")
    
    # Drop modified table
    op.drop_table('devs')
    
    # Rename back to original
    op.rename_table('old_devs', 'devs')
