"""initial tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('one_id_sub', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_one_id_sub', 'users', ['one_id_sub'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('logo_url', sa.String(), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    op.create_table('profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('photo_url', sa.String(), nullable=True),
        sa.Column('profile_type', sa.String(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('skills', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('experience', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('education', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('certificates', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('location_lat', sa.Float(), nullable=True),
        sa.Column('location_lng', sa.Float(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    op.create_table('jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('work_format', sa.String(), nullable=True),
        sa.Column('salary_min', sa.Integer(), nullable=True),
        sa.Column('salary_max', sa.Integer(), nullable=True),
        sa.Column('salary_currency', sa.String(), nullable=True),
        sa.Column('required_skills', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('location_lat', sa.Float(), nullable=True),
        sa.Column('location_lng', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('duration_hours', sa.Integer(), nullable=True),
        sa.Column('has_certificate', sa.Boolean(), nullable=True),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('related_skills', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('biographies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('quote', sa.Text(), nullable=True),
        sa.Column('story', sa.Text(), nullable=True),
        sa.Column('photo_url', sa.String(), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('biographies')
    op.drop_table('courses')
    op.drop_table('jobs')
    op.drop_table('profiles')
    op.drop_table('companies')
    op.drop_table('users')
