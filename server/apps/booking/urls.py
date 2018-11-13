from django.urls import path

from .views.booking import BookingList
from .views.booking import BookingCreate
from .views.campon import CampOnView
from .views.booking import BookingRetrieveUpdateDestroy
from .views.recurring_booking import RecurringBookingView

urlpatterns = [
    path(r'bookings', BookingList.as_view()),
    path(r'booking', BookingCreate.as_view()),
    path(r'booking/<int:pk>', BookingRetrieveUpdateDestroy.as_view()),

    path(r'campon', CampOnView.as_view()),

    path(r'recurring_booking', RecurringBookingView.as_view())
]
