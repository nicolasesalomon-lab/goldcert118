from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    role_enum = sa.Enum("Admin", "Analista", "Consulta", name="role", native_enum=False)
    ambito_enum = sa.Enum("tipo", "marca", name="ambito_certificado", native_enum=False)
    estado_enum = sa.Enum("vigente", "vencido", "suspendido", name="estado_certificacion", native_enum=False)
    tipo_item_enum = sa.Enum(
        "cb",
        "test_report",
        "manual",
        "etiquetas",
        "mapa_modelos",
        "declaracion_identidad",
        "verificacion_identidad",
        name="tipo_item",
        native_enum=False,
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("role", role_enum, nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "organismos_certificacion",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("nombre", name="uq_odc_nombre"),
    )

    op.create_table(
        "proveedores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("telefono", sa.String(), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("nombre", name="uq_proveedor_nombre"),
    )

    op.create_table(
        "fabricas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("proveedor_id", sa.Integer(), sa.ForeignKey("proveedores.id"), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("direccion", sa.String(), nullable=True),
        sa.Column("audit_valida_desde", sa.Date(), nullable=True),
        sa.Column("audit_valida_hasta", sa.Date(), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("proveedor_id", sa.Integer(), sa.ForeignKey("proveedores.id"), nullable=False),
        sa.Column("modelo_proveedor", sa.String(), nullable=True),
        sa.Column("modelo_goldmund", sa.String(), nullable=True),
        sa.Column("odc_id", sa.Integer(), sa.ForeignKey("organismos_certificacion.id"), nullable=True),
    )

    op.create_table(
        "certificaciones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False),
        sa.Column("ambito_certificado", ambito_enum, nullable=False, server_default="tipo"),
        sa.Column("fabrica_id", sa.Integer(), sa.ForeignKey("fabricas.id"), nullable=True),
        sa.Column("valido_desde", sa.Date(), nullable=False),
        sa.Column("valido_hasta", sa.Date(), nullable=False),
        sa.Column("estado", estado_enum, nullable=False, server_default="vigente"),
        sa.Column("creado_en", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "producto_id",
            "ambito_certificado",
            "fabrica_id",
            "valido_desde",
            "valido_hasta",
            name="uq_cert_rango_basico",
        ),
    )

    op.create_table(
        "certificaciones_requisitos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("certificacion_id", sa.Integer(), sa.ForeignKey("certificaciones.id"), nullable=False),
        sa.Column("tipo_item", tipo_item_enum, nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("filename_original", sa.String(), nullable=False),
        sa.Column("uploaded_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("certificacion_id", "tipo_item", name="uq_cert_item_unico"),
    )


def downgrade() -> None:
    op.drop_table("certificaciones_requisitos")
    op.drop_table("certificaciones")
    op.drop_table("productos")
    op.drop_table("fabricas")
    op.drop_table("proveedores")
    op.drop_table("organismos_certificacion")
    op.drop_table("users")
