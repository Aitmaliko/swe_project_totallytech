"""
Скрипт для обновления схемы таблицы complaints
Делает поле order_id необязательным
"""
from sqlalchemy import create_engine, text
from config import settings

def fix_complaint_schema():
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Делаем order_id необязательным
            connection.execute(text(
                "ALTER TABLE complaints ALTER COLUMN order_id DROP NOT NULL"
            ))
            connection.commit()
            print("✅ Схема таблицы complaints успешно обновлена!")
            print("   Поле order_id теперь необязательное")
            
    except Exception as e:
        print(f"❌ Ошибка при обновлении схемы: {e}")
        raise

if __name__ == "__main__":
    fix_complaint_schema()
