"""Initial migration for FastAPI database setup

Revision ID: 580f5165897c
Revises: 
Create Date: 2024-07-03 11:22:33.689505

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '580f5165897c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # If 'nepse' table exists from a previous schema, rename it to 'fastapi'
    # Check if the table exists by attempting to rename it
    # This must be done in a try-except or conditional based on your DB backend capabilities
    # Since Alembic/SQLAlchemy doesn't directly support checking table existence in migrations
    # you may need to handle this logic outside of Alembic or manually ensure it.
    
    # Example of direct renaming (uncomment if you know 'nepse' exists and needs renaming)
    # op.rename_table('nepse', 'fastapi')

    # Alternatively, if creating 'fastapi' afresh
    op.create_table('fastapi',
        sa.Column('Sn', sa.Integer(), nullable=False),
        sa.Column('Symbol', sa.String(), nullable=True),
        sa.Column('Close_Price_Rs', sa.Float(), nullable=True),
        sa.Column('Open_Price_Rs', sa.Float(), nullable=True),
        sa.Column('High_Price_Rs', sa.Float(), nullable=True),
        sa.Column('Low_Price_Rs', sa.Float(), nullable=True),
        sa.Column('Total_Traded_Quantity', sa.Integer(), nullable=True),
        sa.Column('Total_Traded_Value', sa.Float(), nullable=True),
        sa.Column('Total_Trades', sa.Integer(), nullable=True),
        sa.Column('LTP', sa.String(), nullable=True),
        sa.Column('Previous_Day_Close_Price_Rs', sa.Float(), nullable=True),
        sa.Column('Average_Traded_Price_Rs', sa.Float(), nullable=True),
        sa.Column('Fifty_Two_Week_High_Rs', sa.Float(), nullable=True),
        sa.Column('Fifty_Two_Week_Low_Rs', sa.Float(), nullable=True),
        sa.Column('Market_Capitalization_Rs__Amt_in_Millions', sa.Float(), nullable=True),
        sa.Column('Close_Date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('Sn')
    )

def downgrade():
    # Revert renaming or drop 'fastapi' table
    op.drop_table('fastapi')
    
    # If the original 'nepse' needs to be restored from 'fastapi', rename it back
    # op.rename_table('fastapi', 'nepse')

