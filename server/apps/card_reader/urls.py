from django.urls import path

from .views.card_reader import ListCardReaders, CardReaderCreateView, CardReaderUpdateView, CardReaderDeleteView, \
    CardReaderConfirmBookingView

urlpatterns = [
    path(r'card_readers', ListCardReaders.as_view()),
    path(r'card_reader', CardReaderCreateView.as_view()),
    path(r'card_reader/<int:pk>', CardReaderUpdateView.as_view()),
    path(r'card_reader/<int:pk>/delete', CardReaderDeleteView.as_view()),
    path(r'card_reader/card_read', CardReaderConfirmBookingView.as_view())
]
