from django.urls import path

from .views.booking import BookingView
from .views.campon import CampOnView

urlpatterns = [
    path(r'booking', BookingView.as_view()),
    path(r'campon', CampOnView.as_view())
]
