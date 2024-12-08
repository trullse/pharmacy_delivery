from django.views import generic
from pharmacy_delivery.apps.orm.BaseManager import BaseManager
from pharmacy_delivery.apps.products.models import Medicine


class MedicinesIndexView(generic.ListView):
    template_name = "medicines_index.html"
    context_object_name = "medicines_list"

    def get_queryset(self):
        BaseManager.set_connection()
        medicine = Medicine.objects.select('name', 'price')
        print(medicine)
        return medicine


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)