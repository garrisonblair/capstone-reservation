from django.urls import path

from .views.booking import BookingView

urlpatterns = [
    path(r'booking', BookingView.as_view())
]