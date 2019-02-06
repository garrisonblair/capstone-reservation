from django.urls import path
from .views.groups import GroupList, InviteMembers, GroupCreate, RemoveMembers, LeaveGroup

from .views.group_privileges import PrivilegeRequestList, PrivilegeRequestCreate, PrivilegeRequestDelete, \
    MyGroupPrivileges
from .views.group_privileges import ApprovePrivilegeRequest, DenyPrivilegeRequest
from .views.group_invitations import GroupInvitationsList, AcceptInvitation, RejectInvitation, RevokeInvitation


urlpatterns = [
    path(r'group/<int:pk>/invite_members', InviteMembers.as_view()),
    path(r'group/<int:pk>/remove_members', RemoveMembers.as_view()),
    path(r'group', GroupCreate.as_view()),
    path(r'groups', GroupList.as_view()),
    path(r'group/<int:pk>/leave_group', LeaveGroup.as_view()),
    path(r'request_privilege', PrivilegeRequestCreate.as_view()),
    path(r'privilege_requests', PrivilegeRequestList.as_view()),
    path(r'privilege_requests/<str:status>', PrivilegeRequestList.as_view()),
    path(r'approve_privilege_request', ApprovePrivilegeRequest.as_view()),
    path(r'deny_privilege_request', DenyPrivilegeRequest.as_view()),
    path(r'group_invitations', GroupInvitationsList.as_view()),
    path(r'group_invitation/<int:pk>/accept', AcceptInvitation.as_view()),
    path(r'group_invitation/<int:pk>/reject', RejectInvitation.as_view()),
    path(r'group_invitation/<int:pk>/revoke', RevokeInvitation.as_view()),
    path(r'cancel_request/<int:pk>', PrivilegeRequestDelete.as_view()),
    path(r'group/<int:pk>/privileges', MyGroupPrivileges.as_view()),
]
