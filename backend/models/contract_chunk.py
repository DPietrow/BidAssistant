from database import db


class ContractChunk(db.Model):
    __tablename__ = "contract_chunks"

    id = db.Column(db.Integer, primary_key=True)

    contract_id = db.Column(
        db.Integer,
        db.ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    #
    # order within document
    #
    chunk_index = db.Column(
        db.Integer,
        nullable=False,
    )

    #
    # actual text sent to OpenAI
    #
    chunk_text = db.Column(
        db.Text,
        nullable=False,
    )

    #
    # optional metadata
    #
    token_count = db.Column(
        db.Integer,
        default=0,
    )

    embedding_created = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    embedding_model = db.Column(
        db.String(100),
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )

    #
    # relationship
    #
    contract = db.relationship(
        "Contract",
        back_populates="chunks"
    )
    
    embedding = db.relationship(
        "ContractEmbedding",
        back_populates="chunk",
        uselist=False,
        cascade="all, delete-orphan"
    )