from app import create_app
from app.extensions import db
from app.models import User, Book, SwapAdvert, SwapRequest, Review, AIRequest, PasswordResetToken

app = create_app()

with app.app_context():
    print("Подключение к базе:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Создаем таблицы...")
    try:
        db.create_all()
        print("Таблицы успешно созданы (или уже существовали)!")
        
        # Проверяем, какие таблицы сейчас есть в базе
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Список таблиц в базе данных:", tables)
    except Exception as e:
        print("ОШИБКА:", e)