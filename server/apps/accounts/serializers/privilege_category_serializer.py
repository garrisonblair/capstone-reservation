from rest_framework import serializers

from ..models.PrivilegeCategory import PrivilegeCategory


class PrivilegeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    parent_category = serializers.PrimaryKeyRelatedField(queryset=PrivilegeCategory.objects.all())
    max_days_until_booking = serializers.IntegerField(allow_null=True)
    can_make_recurring_booking = serializers.NullBooleanField()
    max_bookings = serializers.IntegerField(allow_null=True)
    max_recurring_bookings = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        return PrivilegeCategory.objects.create(
            name=validated_data["name"],
            parent_category=validated_data["parent_category"],
            max_days_until_booking=validated_data["max_days_until_booking"],
            can_make_recurring_booking=validated_data["can_make_recurring_booking"],
            max_bookings=validated_data["max_bookings"],
            max_recurring_bookings=validated_data["max_recurring_bookings"]
        )

    class Meta:
        model = PrivilegeCategory
        fields = '__all__'
