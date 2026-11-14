from datetime import datetime, timezone
from app.extensions import db

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    discipline = db.Column(db.String(100))
    condition = db.Column(db.String(50), nullable=False)
    ai_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Связи
    owner = db.relationship('User', back_populates='books')
    advert = db.relationship('SwapAdvert', back_populates='book', uselist=False, cascade='all, delete-orphan')