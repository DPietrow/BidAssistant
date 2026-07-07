from sqlalchemy.sql import func

from pgvector.sqlalchemy import Vector

from database import db


class ContractEmbedding(db.Model):

    __tablename__ = "contract_embeddings"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    #
    # One embedding per chunk
    #

    chunk_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "contract_chunks.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True,
        index=True
    )


    #
    # Embedding metadata
    #

    model = db.Column(
        db.String(100),
        nullable=False,
        default="text-embedding-3-small"
    )


    dimensions = db.Column(
        db.Integer,
        nullable=False,
        default=1536
    )


    #
    # Vector stored in pgvector
    #

    embedding = db.Column(
        Vector(1536),
        nullable=False
    )


    #
    # Versioning
    # Useful later if you change models
    #

    embedding_version = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )


    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )


    #
    # Relationship
    #

    chunk = db.relationship(
        "ContractChunk",
        back_populates="embedding"
    )


    __table_args__ = (

        db.Index(
            "embedding_vector_idx",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_ops={
                "embedding": "vector_cosine_ops"
            }
        ),

    )