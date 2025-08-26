import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    """Возвращает соединение с базой данных"""
    # Получаем строку подключения от Render
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Парсим URL от Render
        result = urlparse(database_url)
        return psycopg2.connect(
            host=result.hostname,
            database=result.path[1:],  # Убираем первый слэш
            user=result.username,
            password=result.password,
            port=result.port
        )
    else:
        # Локальная разработка
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'school_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
    
    
def init_db():
    """Инициализирует базу данных и таблицы"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Создаем таблицу schools
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schools (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Проверяем, есть ли тестовые данные
            cur.execute("SELECT COUNT(*) FROM schools")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO schools (id, name, type) VALUES
                    ('1', 'Hexlet', 'programming'),
                    ('2', 'Netology', 'management'),
                    ('3', 'Stepik', 'education')
                """)
            
        conn.commit()
        print("База данных инициализирована успешно!")
        
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Testing database functions...")
    init_db()
    print("init_db function exists and works!")