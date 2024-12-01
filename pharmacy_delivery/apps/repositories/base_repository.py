import psycopg2
from psycopg2.extras import RealDictCursor

DB_SETTINGS = {
    'dbname': 'pharmacydb',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1',
    'port': '5432',
}

def connect_to_db():
    try:
        db_connection = psycopg2.connect(**DB_SETTINGS)
        print("Database connection successful.")
        return db_connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        raise


class BaseRepository:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def fetch_one(self, query, params=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            result = cursor.fetchone()
        return result

    def fetch_all(self, query, params=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results

    def execute(self, query, params=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or [])
        self.connection.commit()

    def insert(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        params = tuple(kwargs.values())
        self.execute(query, params)

    def get_by_id(self, record_id):
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        return self.fetch_one(query, [record_id])

    def get_all(self):
        query = f"SELECT * FROM {self.table_name}"
        return self.fetch_all(query)

    def update(self, record_id, **kwargs):
        columns = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE {self.table_name} SET {columns} WHERE id = %s"
        params = tuple(kwargs.values()) + (record_id,)
        self.execute(query, params)

    def delete(self, record_id):
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        self.execute(query, [record_id])
