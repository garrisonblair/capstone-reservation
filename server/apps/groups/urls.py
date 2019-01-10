from django.urls import path
from .views.groups import GroupList, AddMembers, GroupCreate, RemoveMembers, LeaveGroup
from .views.group_privileges import PrivilegeRequestList, PrivilegeRequestCreate
from .views.group_privileges import ApprovePrivilegeRequest, DenyPrivilegeRequest


urlpatterns = [
    path(r'group/<int:pk>/add_members', AddMembers.as_view()),
    path(r'group/<int:pk>/remove_members', RemoveMembers.as_view()),
    path(r'group', GroupCreate.as_view()),
    path(r'groups', GroupList.as_view()),
    path(r'group/<int:pk>/leave_group', LeaveGroup.as_view()),
    path(r'request_privilege', PrivilegeRequestCreate.as_view()),
    path(r'privilege_requests', PrivilegeRequestList.as_view()),
    path(r'privilege_requests/<str:status>', PrivilegeRequestList.as_view()),
    path(r'approve_privilege_request', ApprovePrivilegeRequest.as_view()),
    path(r'deny_privilege_request', DenyPrivilegeRequest.as_view())
]
