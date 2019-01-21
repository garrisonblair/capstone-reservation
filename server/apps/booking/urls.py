from django.urls import path

from .views.booking import BookingList
from .views.booking import BookingCreate, BookingRetrieveUpdateDestroy, BookingViewMyBookings
from .views.campon import CampOnList
from .views.campon import CampOnCreate
from .views.recurring_booking import RecurringBookingCreate

urlpatterns = [
    path(r'bookings', BookingList.as_view()),
    path(r'booking', BookingCreate.as_view()),
    path(r'booking/<int:pk>', BookingRetrieveUpdateDestroy.as_view()),
    path(r'my_bookings/', BookingViewMyBookings.as_view()),
    path(r'campons', CampOnList.as_view()),
    path(r'campon', CampOnCreate.as_view()),
    path(r'recurring_booking', RecurringBookingCreate.as_view())
]
