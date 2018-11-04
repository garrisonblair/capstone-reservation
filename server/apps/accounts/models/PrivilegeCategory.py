from django.db import models


class PrivilegeCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    parent_category = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    # rule parameter fields
    # When you add a field, update model test testCreation to check its defaulted to None
    # (Important for delegation to parent category)
    num_days_to_booking = models.PositiveIntegerField(null=True)
    can_make_recurring_booking = models.BooleanField(null=True)
    max_num_bookings = models.PositiveIntegerField(null=True)
    max_num_recurring_bookings = models.PositiveIntegerField(null=True)

    def get_parameter(self, param_name):
        value = getattr(self, param_name)

        if value is not None:
            return value

        value = self.parent_category.get_parameter(param_name)

        if value is None:
            raise Exception()

        return value

    def get_error_text(self, param_name):

        error_messages = {
            "num_days_to_booking": "Attempting to book too many days in advance. Maximum: " +
                                   str(self.num_days_to_booking),
            "can_make_recurring_bookings": "Not permitted to make recurring bookings.",
            "max_num_bookings": "Booker has too many bookings. Maximum: " + str(self.max_num_bookings),
            "max_num_recurring_bookings": "Booker has too many recurring bookings. Maximum: " +
                                          str(self.max_num_recurring_bookings)
        }

        return error_messages.get(param_name)

    def __str__(self):
        return self.name + " parent category: " + self.parent_category.name
