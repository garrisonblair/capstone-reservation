from django.urls import path

from .views.room import RoomView

urlpatterns = [
    path(r'room', RoomView.as_view()),
    path(r'room/<start_date_time>/<end_date_time>/', RoomView.as_view()),
]