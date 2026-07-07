from database import db
from sqlalchemy.sql import func


class Contract(db.Model):

    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)

    # -----------------------
    # Identity
    # -----------------------

    sam_id = db.Column(db.String(100), unique=True, nullable=False)

    url = db.Column(db.Text)

    source = db.Column(db.String(50), default="SAM.gov")

    # -----------------------
    # Contract Info
    # -----------------------

    title = db.Column(db.String(500), nullable=False)

    description = db.Column(db.Text)

    raw_text = db.Column(db.Text)

    agency = db.Column(db.String(200))

    office = db.Column(db.String(200))

    naics = db.Column(db.String(20))

    notice_type = db.Column(db.String(100))

    set_aside = db.Column(db.String(100))

    status = db.Column(db.String(50))

    estimated_value = db.Column(db.String(100))

    estimated_value_text = db.Column(db.String(100))

    solicitation_number = db.Column(db.String(100))

    psc_code = db.Column(db.String(20))

    # -----------------------
    # Dates
    # -----------------------

    posted_date = db.Column(db.Date)

    close_date = db.Column(db.Date)

    response_deadline = db.Column(db.DateTime)

    # -----------------------
    # AI Pipeline
    # -----------------------

    chunk_count = db.Column(
        db.Integer,
        default=0,
    )

    embedding_model = db.Column(db.String(100))

    embedding_version = db.Column(
        db.Integer,
        default=1
    )

    embedding_status = db.Column(
        db.String(25),
        default="pending"
    )

    embedded_at = db.Column(
        db.DateTime
    )

    embedding_error = db.Column(
        db.Text
    )

    # Added later

    bid_score = db.Column(db.Float)

    biddability_tier = db.Column(db.String(20))

    proposal_generated = db.Column(db.Boolean, default=False)

    proposal_submitted = db.Column(db.Boolean, default=False)


    # -----------------------
    # Metadata
    # -----------------------

    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    chunks = db.relationship(
        "ContractChunk",
        back_populates="contract",
        cascade="all, delete-orphan",
        lazy=True
    )