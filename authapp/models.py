from pharmacy_delivery.apps.orm.BaseModel import BaseModel


class User(BaseModel):
    table_name = "user"

class Role(BaseModel):
    table_name = "role"
