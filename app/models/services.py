import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from app.extensions import db
from app.models.user import PasswordResetToken, User

TOKEN_TTL_MINUTES = 30

def create_reset_token(email):
    """Генерирует токен для сброса пароля и сохраняет его хеш в БД."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None  # Возвращаем None, чтобы не раскрывать существование email

    # 1. Генерируем криптографически стойкий токен
    raw_token = secrets.token_urlsafe(32)
    
    # 2. Хешируем его (в БД попадет только хеш)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    
    # 3. Сохраняем в базу
    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES)
    )
    db.session.add(reset_token)
    db.session.commit()
    
    return raw_token

def verify_reset_token(raw_token):
    """Проверяет токен из ссылки и возвращает пользователя, если токен валиден."""
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    
    token_record = PasswordResetToken.query.filter_by(token_hash=token_hash).first()
    if not token_record:
        return None 
        
    if token_record.expires_at < datetime.now(timezone.utc):
        return None 
        
    if token_record.used_at is not None:
        return None 
        
    return token_record.user