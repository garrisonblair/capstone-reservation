from django.urls import path
from apps.statistics.views.room_statistics import RoomStatistics
from apps.statistics.views.program_statistics import ProgramStatistics


urlpatterns = [
    path(r'room_statistics', RoomStatistics.as_view()),
    path(r'program_statistics', RoomStatistics.as_view())
]
