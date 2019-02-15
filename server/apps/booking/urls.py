from django.urls import path

from .views.booking import BookingRetrieveUpdateDestroy, BookingViewMyBookings
from .views.booking import BookingList, BookingCreate, BookingCancel
from .views.campon import CampOnList
from .views.campon import CampOnCreate
from .views.recurring_booking import RecurringBookingCreate

urlpatterns = [
    path(r'bookings', BookingList.as_view()),
    path(r'booking', BookingCreate.as_view()),
    path(r'booking/<int:pk>', BookingRetrieveUpdateDestroy.as_view()),
    path(r'bookings/<int:pk>', BookingViewMyBookings.as_view()),
    path(r'booking/<int:pk>/cancel_booking', BookingCancel.as_view()),
    path(r'campons', CampOnList.as_view()),
    path(r'campon', CampOnCreate.as_view()),
    path(r'recurring_booking', RecurringBookingCreate.as_view())
]
