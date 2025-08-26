import psycopg2
from psycopg2.extras import DictCursor
from .database import get_connection
import uuid


class SchoolRepository():


    def __init__(self):
        self.conn = get_connection()


    def find_all(self):
        with self.conn.cursor(cursor_factory = DictCursor) as cursor:
            cursor.execute("SELECT * FROM schools")
            return [dict(row) for row in cursor]


    def find_by_id(self, school_id):
        with self.conn.cursor(cursor_factory = DictCursor) as cursor:
            cursor.execute("SELECT * FROM schools WHERE id =%s", (school_id,))
            row = cursor.fetchone()
            return dict(row) if row else None


    def _create(self, school_data):
        with self.conn.cursor() as cursor:
            school_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO schools (id, name, type) VALUES( %s, %s, %s)",
                (school_id, school_data["name"], school_data["type"])
            )
            school_data["id"] = school_id
        self.conn.commit()
    

    def update(self,school_id, school_data):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE schools SET name = %s, type = %s WHERE id = %s",
                (school_data["name"], school_data["type"], school_id)
            )
        self.conn.commit()


    def save(self, school_data):
        if "id" in school_data and school_data["id"]:
            self.update(school_data)
        else:
            self._create(school_data)


    def delete(self, school_id):
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM schools WHERE id = %s", (school_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
