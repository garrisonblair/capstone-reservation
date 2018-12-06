from django.urls import path
from .views.groups import GroupList, AddMembers, GroupCreate, RemoveMembers


urlpatterns = [
    path(r'group/<int:pk>/add_members', AddMembers.as_view()),
    path(r'group/<int:pk>/remove_members', RemoveMembers.as_view()),
    path(r'group', GroupCreate.as_view()),
    path(r'groups', GroupList.as_view())
]
