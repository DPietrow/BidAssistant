from sqlalchemy.sql import func

from pgvector.sqlalchemy import Vector

from database import db


class ContractEmbedding(db.Model):

    __tablename__ = "contract_embeddings"

    id = db.Column(db.Integer, primary_key=True)

    chunk_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "contract_chunks.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    model = db.Column(
        db.String(100),
        nullable=False
    )

    dimensions = db.Column(
        db.Integer,
        nullable=False,
        default=1536
    )

    embedding = db.Column(
        Vector(1536),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )