from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Инициализация базы данных - создание таблиц если их нет"""
    try:
        # Импортируем все модели чтобы они зарегистрировались
        from models import User, Supplier, Consumer, Link, Product, Order, OrderItem, Message, Complaint
        
        # Создаем таблицы если их нет
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise

def get_db():
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
