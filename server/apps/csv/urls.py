from django.urls import path
from apps.csv.views.csv import CsvView

urlpatterns = [
    path(r'csv', CsvView.as_view()),
]
