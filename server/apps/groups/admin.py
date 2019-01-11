from django.contrib import admin
from .models.Group import Group
from .models.PrivilegeRequest import PrivilegeRequest
from .models.GroupInvitation import GroupInvitation


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'privilege_category', 'is_verified')


class PrivilegeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'privilege_category', 'submission_date', 'status')


class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'invited_booker', 'timestamp')


admin.site.register(Group, GroupAdmin)
admin.site.register(PrivilegeRequest, PrivilegeRequestAdmin)
admin.site.register(GroupInvitation, GroupInvitationAdmin)
