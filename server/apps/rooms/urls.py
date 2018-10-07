from django.urls import path

from .views.room import RoomView

urlpatterns = [
    path(r'room', RoomView.as_view())
]