from django.db import models

from apps.util.comparators import *
from apps.util.AbstractPrivilege import AbstractPrivilege


class FieldMetadata:

    def __init__(self, error_message, comparator):
        self.error_message = error_message
        self.comparator = comparator
        pass


class PrivilegeCategory(models.Model, AbstractPrivilege):
    name = models.CharField(max_length=100, blank=False, unique=True)
    parent_category = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    # rule parameter fields
    # When you add a field, update model test testCreation to check its defaulted to None
    # (Important for delegation to parent category)
    max_days_until_booking = models.PositiveIntegerField(null=True, blank=True)
    can_make_recurring_booking = models.BooleanField(null=True, blank=True)
    max_bookings = models.PositiveIntegerField(null=True, blank=True)
    max_recurring_bookings = models.PositiveIntegerField(null=True, blank=True)

    booking_start_time = models.TimeField(null=True, blank=True)
    booking_end_time = models.TimeField(null=True, blank=True)

    field_metadata = {
        "max_days_until_booking": FieldMetadata(
            error_message="Attempting to book too many days in advance.",
            comparator=IntegerComparator(bigger_better=True)
        ),
        "can_make_recurring_booking": FieldMetadata(
            error_message="Not permitted to make recurring bookings.",
            comparator=BooleanComparator()
        ),
        "max_bookings": FieldMetadata(
            error_message="Booker has too many bookings. Maximum: ",
            comparator=IntegerComparator()
        ),
        "max_recurring_bookings": FieldMetadata(
            error_message="Booker has too many recurring bookings.",
            comparator=IntegerComparator()
        ),
        "booking_start_time": FieldMetadata(
            error_message="Booking too early",
            comparator=TimeComparator(earlier_better=True)
        ),
        "booking_end_time": FieldMetadata(
            error_message="Booking Too Late",
            comparator=TimeComparator(earlier_better=False)
        )
    }

    def save(self, *args, **kwargs):

        if self.is_default:
            try:
                current_default = PrivilegeCategory.objects.get(is_default=True)
                current_default.is_default = False
                current_default.save()
            except PrivilegeCategory.DoesNotExist:
                pass

        return super(PrivilegeCategory, self).save(*args, **kwargs)

    def get_parameter(self, param_name):
        value = getattr(self, param_name)
        if value is not None:
            return value

        value = self.parent_category.get_parameter(param_name)

        if value is None:
            raise Exception()

        return value

    def get_error_text(self, param_name):

        # error_messages = {
        #     "max_days_until_booking": "Attempting to book too many days in advance. Maximum: " +
        #                               str(self.max_days_until_booking),
        #     "can_make_recurring_bookings": "Not permitted to make recurring bookings.",
        #     "max_bookings": "Booker has too many bookings. Maximum: " + str(self.max_bookings),
        #     "max_recurring_bookings": "Booker has too many recurring bookings. Maximum: " +
        #                               str(self.max_recurring_bookings),
        #
        #     "booking_start_time": "Cannot book before " + str(self.booking_start_time),
        #     "booking_end_time": "Cannot book after " + str(self.booking_end_time)
        # }

        return self.field_metadata.get(param_name).error_message

    def __str__(self):
        value = self.name
        if self.parent_category is not None:
            value += " parent category: " + self.parent_category.name
        return value


class PrivilegeMerger(AbstractPrivilege):

    def __init__(self, privilege_set):
        self.privilege_set = privilege_set

    def get_parameter(self, param_name):
        field_comparator = PrivilegeCategory.field_metadata[param_name].comparator  # type: AbstractComparator

        value = self.privilege_set[0].get_parameter(param_name)
        for privilege in self.privilege_set:  # type: PrivilegeCategory
            privilege_value = privilege.get_parameter(param_name)

            if field_comparator.compare(value, privilege_value) < 0:
                value = privilege_value

        return value

    def get_error_text(self, param_name):
        return PrivilegeCategory.field_metadata[param_name].error_message
