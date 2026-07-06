from database import db


class Contract(db.Model):

    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)

    sam_id = db.Column(db.String(100), unique=True)

    title = db.Column(db.String(500))

    description = db.Column(db.Text)

    agency = db.Column(db.String(200))

    naics = db.Column(db.String(20))

    posted_date = db.Column(db.Date)

    close_date = db.Column(db.Date)

    url = db.Column(db.Text)

    raw_text = db.Column(db.Text)

    semantic_score = db.Column(db.Float)

    bid_score = db.Column(db.Float)