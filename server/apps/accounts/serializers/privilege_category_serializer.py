from rest_framework import serializers

from ..models.PrivilegeCategory import PrivilegeCategory


class PrivilegeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    parent_category = serializers.PrimaryKeyRelatedField(queryset=PrivilegeCategory.objects.all())
    num_days_to_booking = serializers.IntegerField(allow_null=True)
    can_make_recurring_booking = serializers.NullBooleanField()
    max_num_bookings = serializers.IntegerField(allow_null=True)
    max_num_recurring_bookings = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        return PrivilegeCategory.objects.create(
            name=validated_data["name"],
            parent_category=validated_data["parent_category"],
            num_days_to_booking=validated_data["num_days_to_booking"],
            can_make_recurring_booking=validated_data["can_make_recurring_booking"],
            max_num_bookings=validated_data["max_num_bookings"],
            max_num_recurring_bookings=validated_data["max_num_recurring_bookings"]
        )

    class Meta:
        model = PrivilegeCategory
        fields = '__all__'
