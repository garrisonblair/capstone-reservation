from django.urls import path

from .views.room import RoomList
from .views.room import RoomCreate
from .views.room import RoomRetrieveUpdateDestroy


urlpatterns = [
    path(r'rooms', RoomList.as_view()),
    path(r'room', RoomCreate.as_view()),
    path(r'room/<int:pk>', RoomRetrieveUpdateDestroy.as_view())
]
