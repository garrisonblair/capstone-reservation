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
    max_bookings = serializers.IntegerField(allow_null=True, required=False)
    max_recurring_bookings = serializers.IntegerField(allow_null=True, required=False)
    booking_start_time = serializers.TimeField(allow_null=True, required=False)
    booking_end_time = serializers.TimeField(allow_null=True, required=False)

    class Meta:
        model = PrivilegeCategory
        fields = '__all__'
