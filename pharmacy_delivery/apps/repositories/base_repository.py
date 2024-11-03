from django.db import connection, transaction

class BaseRepository:
    def __init__(self, table_name):
        self.table_name = table_name

    def fetch_one(self, query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            result = cursor.fetchone()
        return result

    def fetch_all(self, query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results

    def execute(self, query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
        transaction.commit()

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
