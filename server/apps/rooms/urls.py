from django.urls import path
# from django.urls import re_path

from .views.room import RoomView
from .views.room import RoomDeleteView
from .views.room import RoomUpdateView
from .views.room import RoomCreateView


urlpatterns = [
    path(r'room', RoomView.as_view()),
    path(r'roomcreate', RoomCreateView.as_view()),
    path(r'roomdelete', RoomDeleteView.as_view()),
    path(r'roomupdate', RoomUpdateView.as_view()),
]
