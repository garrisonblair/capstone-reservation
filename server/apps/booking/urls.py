from django.urls import path

from .views.booking import BookingView
from .views.recurring_booking import RecurringBookingView

urlpatterns = [
    path(r'booking', BookingView.as_view()),
    path(r'recurring_booking', RecurringBookingView.as_view())
]
