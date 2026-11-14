from datetime import datetime, timezone
from app.extensions import db

class SwapAdvert(db.Model):
    __tablename__ = 'swap_adverts'
    
    id = db.Column(db.BigInteger, primary_key=True)
    book_id = db.Column(db.BigInteger, db.ForeignKey('books.id', ondelete='CASCADE'), unique=True, nullable=False)
    owner_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    wish_conditions = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    book = db.relationship('Book', back_populates='advert')
    requests = db.relationship('SwapRequest', back_populates='advert', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint("status IN ('active', 'reserved', 'completed', 'cancelled')", name='ck_swap_adverts_status'),
    )

class SwapRequest(db.Model):
    __tablename__ = 'swap_requests'
    
    id = db.Column(db.BigInteger, primary_key=True)
    advert_id = db.Column(db.BigInteger, db.ForeignKey('swap_adverts.id', ondelete='CASCADE'), nullable=False, index=True)
    requester_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    advert = db.relationship('SwapAdvert', back_populates='requests')
    review = db.relationship('Review', back_populates='request', uselist=False, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name='ck_swap_requests_status'),
    )

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.BigInteger, primary_key=True)
    request_id = db.Column(db.BigInteger, db.ForeignKey('swap_requests.id', ondelete='CASCADE'), unique=True, nullable=False)
    author_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    request = db.relationship('SwapRequest', back_populates='review')
    
    __table_args__ = (
        db.CheckConstraint("rating >= 1 AND rating <= 5", name='ck_reviews_rating'),
    )