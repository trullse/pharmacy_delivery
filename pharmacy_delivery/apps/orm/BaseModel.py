from pharmacy_delivery.apps.orm.BaseManager import BaseManager


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        # attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        # return f"<{self.__class__.__name__}: ({attrs_format})>\n"
        return self.__dict__.items()
