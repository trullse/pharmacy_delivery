from .base_repository import BaseRepository


class MedicineRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection, 'medicine')

    def get_medicines_by_category(self, category_id):
        query = "SELECT * FROM medicine WHERE category_id = %s"
        return self.fetch_all(query, [category_id])
