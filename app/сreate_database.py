import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Создает базу данных если она не существует"""
    try:
        # Подключаемся к базе postgres по умолчанию
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database='postgres',  # Подключаемся к стандартной БД
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', '5432')
        )
        conn.autocommit = True  # Для создания БД нужен autocommit
        
        with conn.cursor() as cur:
            # Проверяем существование базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'school_db'")
            exists = cur.fetchone()
            
            if not exists:
                # Создаем базу данных
                cur.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier('school_db')
                ))
                print("✅ База данных 'school_db' создана успешно!")
            else:
                print("✅ База данных 'school_db' уже существует")
                
    except Exception as e:
        print(f"❌ Ошибка при создании БД: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_database()