from rest_framework import serializers
from ..models.PrivilegeRequest import PrivilegeRequest

from apps.groups.serializers.group import WriteGroupSerializer
from apps.accounts.serializers.privilege_category import PrivilegeCategorySerializer


class WritePrivilegeRequestSerializer(serializers.ModelSerializer):

    group = WriteGroupSerializer()
    privilege_category = PrivilegeCategorySerializer()

    class Meta:
        model = PrivilegeRequest
        fields = '__all__'


class ReadPrivilegeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivilegeRequest
        fields = '__all__'
