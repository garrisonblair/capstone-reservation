from django.urls import path
from apps.statistics.views.room_statistics import RoomStatistics


urlpatterns = [
    path(r'room_statistics', RoomStatistics.as_view())
]
