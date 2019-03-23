from rest_framework import serializers

from ..models.PrivilegeCategory import PrivilegeCategory


class PrivilegeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    parent_category = serializers.PrimaryKeyRelatedField(queryset=PrivilegeCategory.objects.all(),
                                                         allow_null=True,
                                                         required=False)
    is_default = serializers.NullBooleanField(required=False)
    max_days_until_booking = serializers.IntegerField(allow_null=True, required=False)
    can_make_recurring_booking = serializers.NullBooleanField(required=False)
    max_recurring_bookings = serializers.IntegerField(allow_null=True, required=False)
    booking_start_time = serializers.TimeField(allow_null=True, required=False)
    booking_end_time = serializers.TimeField(allow_null=True, required=False)

    class Meta:
        model = PrivilegeCategory
        fields = '__all__'


class ReadPrivilegeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    parent_category = PrivilegeCategorySerializer(required=False)
    is_default = serializers.NullBooleanField(required=False)
    max_days_until_booking = serializers.IntegerField(allow_null=True, required=False)
    can_make_recurring_booking = serializers.NullBooleanField(required=False)
    max_recurring_bookings = serializers.IntegerField(allow_null=True, required=False)
    booking_start_time = serializers.TimeField(allow_null=True, required=False)
    booking_end_time = serializers.TimeField(allow_null=True, required=False)

    inherited_values = serializers.SerializerMethodField()

    def get_inherited_values(self, privilege):
        inherited_values = dict()
        for param_name in PrivilegeCategory.get_parameter_names():
            if getattr(privilege, param_name) is None:
                inherited_values[param_name] = privilege.get_parameter(param_name)

        return inherited_values

    class Meta:
        model = PrivilegeCategory
        fields = '__all__'
