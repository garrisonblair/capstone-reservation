from django.urls import path

from .views.room import RoomList
from .views.room import RoomCreate
from .views.room import RoomRetrieveUpdateDestroy
from .views.room_unavailability import RoomUnavailabilityList
from .views.room_unavailability import RoomUnavailabilityCreate
from .views.room_unavailability import RoomUnavailabilityRetrieveUpdateDestroy


urlpatterns = [
    path(r'rooms', RoomList.as_view()),
    path(r'room', RoomCreate.as_view()),
    path(r'room/<int:pk>', RoomRetrieveUpdateDestroy.as_view()),
    path(r'room_unavailabilities', RoomUnavailabilityList.as_view()),
    path(r'room_unavailability', RoomUnavailabilityCreate.as_view()),
    path(r'room_unavailability/<int:pk>', RoomUnavailabilityRetrieveUpdateDestroy.as_view()),
]
