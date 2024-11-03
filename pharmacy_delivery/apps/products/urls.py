from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    # ex: /products/
    path('', views.MedicinesIndexView.as_view(), name="medicine_index"),
]