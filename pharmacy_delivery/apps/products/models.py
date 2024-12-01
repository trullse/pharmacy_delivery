from pharmacy_delivery.apps.orm.BaseModel import BaseModel


class Medicine(BaseModel):
    table_name = "medicine"


class Category(BaseModel):
    table_name = "category"


class CategoryMedicine(BaseModel):
    table_name = "category_medicine"


class Feedback(BaseModel):
    table_name = "feedback"


class Log(BaseModel):
    table_name = "log"


class PharmacyDepartment(BaseModel):
    table_name = "pharmacy_department"


class Role(BaseModel):
    table_name = "role"


class Sale(BaseModel):
    table_name = "sale"


class SaleMedicine(BaseModel):
    table_name = "sale_medicine"


class Supplier(BaseModel):
    table_name = "supplier"


class SupplierDelivery(BaseModel):
    table_name = "supplier_delivery"


class User(BaseModel):
    table_name = '"user"'
