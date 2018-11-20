from django.contrib import admin
from .models.Group import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'privilege_category', 'is_verified')


admin.site.register(Group, GroupAdmin)
