from django.urls import path
from .views.groups import GroupList


urlpatterns = [
    path(r'groups', GroupList.as_view())
]
