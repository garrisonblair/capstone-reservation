from django.urls import path
# from django.urls import re_path

from .views.room import RoomView
from .views.room import RoomDeleteView
from .views.room import RoomUpdateView
from .views.room import RoomCreateView


urlpatterns = [
    path(r'room', RoomView.as_view()),
    path(r'roomcreate', RoomCreateView.as_view()),
    path(r'room/)', RoomDeleteView.as_view()),
    path(r'room/', RoomUpdateView.as_view()),
    path(r'room/', RoomCreateView.as_view()),

    # path(r'room', RoomView),
    # path(r'room/)', RoomDeleteView),
    # path(r'room/', RoomUpdateView),
    # path(r'room/', RoomCreateView),
    # re_path(r'^room/$)', RoomDeleteView.as_view()),
    # re_path(r'^room/$', RoomUpdateView.as_view()),
    # re_path(r'^room/$', RoomCreateView.as_view()),
    # path(r'room/', RoomCreateView.as_view({'post': 'post', 'get': 'get', 'patch': 'patch', 'delete': 'delete'})),
    # path(r'http://localhost:8000/room', RoomCreateView.as_view()),
    # path(r'/room', RoomView.as_view()),
    # path(r'/room/)', RoomDeleteView.as_view()),
    # path(r'/room/', RoomUpdateView.as_view()),
    # path(r'/room/', RoomCreateView.as_view()),
    # path(r'/room)', RoomDeleteView.as_view()),
    # path(r'/room', RoomUpdateView.as_view()),
    # path(r'/room', RoomCreateView.as_view()),
    # path(r'room/<str:room_id>', RoomDeleteView.as_view()),
    # path(r'room/<str:room_id>', RoomUpdateView.as_view()),
    # path(r'room/<int:capacity>', RoomUpdateView.as_view()),
    # path(r'room/<int:number_of_computers>', RoomUpdateView.as_view()),
    # path(r'room/<int:pk>', RoomDeleteView.as_view()),
    # path(r'room/<int:pk>', RoomCreateView.as_view()),
    # path(r'^room/post/$', RoomCreateView.as_view(), name='post'),
    # path(r'^room/$', RoomCreateView.as_view(), name='post'),
    # path(r'^room/$', RoomCreateView.as_view()),
]
