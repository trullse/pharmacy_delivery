from django.views import generic

from pharmacy_delivery.apps.repositories.base_repository import connect_to_db
from pharmacy_delivery.apps.repositories.medicine_repository import MedicineRepository


class MedicinesIndexView(generic.ListView):
    template_name = "medicines_index.html"
    context_object_name = "medicines_list"

    def get_queryset(self):
        connection = connect_to_db()
        medicine_repo = MedicineRepository(connection)
        return medicine_repo.get_all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)