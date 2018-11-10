from django.urls import path

from .views.room import RoomView
from .views.room import RoomDeleteView
from .views.room import RoomUpdateView


urlpatterns = [
    path(r'room', RoomView.as_view()),
    path(r'room/', RoomDeleteView.as_view()),
    path(r'room/', RoomUpdateView.as_view()),
    path(r'room/<str:room_id>', RoomDeleteView.as_view()),
    path(r'room/<str:room_id>', RoomUpdateView.as_view()),
    path(r'room/<int:capacity>', RoomUpdateView.as_view()),
    path(r'room/<int:number_of_computers>', RoomUpdateView.as_view()),

]
