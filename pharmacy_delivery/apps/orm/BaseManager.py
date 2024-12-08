import os
import json
import psycopg2

from django.conf import settings


class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls):
        db_config_path = os.path.join(settings.BASE_DIR, 'db_config.json')
        with open(db_config_path) as file:
            data = json.load(file)
        connection = psycopg2.connect(**data)
        connection.autocommit = True
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)

    @classmethod
    def execute_query_and_out(cls, query, params=None, field_names: list = None, chunk_size=2000):
        cursor = cls._get_cursor()
        cursor.execute(query, params)

        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                # model_objects.append(self.model_class(**row_data))
                model_objects.append(row_data)
            is_fetching_completed = len(result) < chunk_size
        return model_objects

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, condition='', chunk_size=2000):
        fields_format = ', '.join(field_names)
        if condition != '':
            condition = f'WHERE {condition}'
        query = f'SELECT {fields_format} FROM "{self.model_class.table_name}" {condition}'

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)

        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                # model_objects.append(self.model_class(**row_data))
                model_objects.append(row_data)
            is_fetching_completed = len(result) < chunk_size

        return model_objects

    def insert(self, value):
        field_names = value.keys()

        fields_format = ", ".join(field_names)
        values_placeholder_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'])
        query = f'INSERT INTO "{self.model_class.table_name}" ({fields_format}) ' \
                f'VALUES {values_placeholder_format}'

        params = [value[field_name] for field_name in field_names]

        self.execute_query(query, params)

    def insert_list(self, rows: list):
        field_names = rows[0].keys()
        assert all(row.keys() == field_names for row in rows[1:])

        fields_format = ", ".join(field_names)
        values_placeholder_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'] * len(rows))
        query = f'INSERT INTO "{self.model_class.table_name}" ({fields_format}) ' \
                f'VALUES {values_placeholder_format}'

        params = list()
        for row in rows:
            row_values = [row[field_name] for field_name in field_names]
            params += row_values

        self.execute_query(query, params)

    def update(self, new_data: dict):
        field_names = new_data.keys()
        placeholder_format = ', '.join([f'{field_name} = %s' for field_name in field_names])
        query = f'UPDATE "{self.model_class.table_name}" SET {placeholder_format}'
        params = list(new_data.values())

        self.execute_query(query, params)

    def delete(self, condition=''):
        if condition != '':
            condition = f'WHERE {condition}'
        query = f'DELETE FROM "{self.model_class.table_name}" {condition}'

        self.execute_query(query)