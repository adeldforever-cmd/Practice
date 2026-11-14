from datetime import datetime, timezone
from app.extensions import db

class AIRequest(db.Model):
    __tablename__ = 'ai_requests'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    request_type = db.Column(db.String(20), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    output_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    __table_args__ = (
        db.CheckConstraint("request_type IN ('description', 'match')", name='ck_ai_requests_type'),
    )