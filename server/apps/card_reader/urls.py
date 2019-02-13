from django.urls import path

from .views.card_reader import ListCardReaders

urlpatterns = [
    path(r'card_readers', ListCardReaders.as_view()),
]
