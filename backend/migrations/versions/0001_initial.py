from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True),
        sa.Column('name', sa.String),
        sa.Column('role', sa.String),
        sa.Column('password_hash', sa.String),
        sa.Column('created_at', sa.DateTime)
    )
    op.create_table('odc',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nombre', sa.String, unique=True),
        sa.Column('creado_en', sa.DateTime)
    )
    op.create_table('providers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nombre', sa.String, unique=True),
        sa.Column('email', sa.String),
        sa.Column('telefono', sa.String),
        sa.Column('creado_en', sa.DateTime)
    )
    op.create_table('factories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('proveedor_id', sa.Integer, sa.ForeignKey('providers.id')),
        sa.Column('nombre', sa.String),
        sa.Column('direccion', sa.String),
        sa.Column('audit_valida_desde', sa.Date),
        sa.Column('audit_valida_hasta', sa.Date),
        sa.Column('creado_en', sa.DateTime)
    )
    op.create_table('products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nombre', sa.String),
        sa.Column('proveedor_id', sa.Integer, sa.ForeignKey('providers.id')),
        sa.Column('modelo_proveedor', sa.String),
        sa.Column('modelo_goldmund', sa.String),
        sa.Column('odc_id', sa.Integer, sa.ForeignKey('odc.id'))
    )
    op.create_table('certifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('producto_id', sa.Integer, sa.ForeignKey('products.id')),
        sa.Column('ambito_certificado', sa.String),
        sa.Column('fabrica_id', sa.Integer, sa.ForeignKey('factories.id'), nullable=True),
        sa.Column('valido_desde', sa.Date),
        sa.Column('valido_hasta', sa.Date),
        sa.Column('estado', sa.String),
        sa.Column('creado_en', sa.DateTime)
    )
    op.create_table('certification_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('certificacion_id', sa.Integer, sa.ForeignKey('certifications.id')),
        sa.Column('tipo_item', sa.String),
        sa.Column('file_path', sa.String),
        sa.Column('filename_original', sa.String),
        sa.Column('uploaded_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('uploaded_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('certification_items')
    op.drop_table('certifications')
    op.drop_table('products')
    op.drop_table('factories')
    op.drop_table('providers')
    op.drop_table('odc')
    op.drop_table('users')
