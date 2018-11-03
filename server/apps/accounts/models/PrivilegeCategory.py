from django.db import models


class PrivilegeCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    parent_category = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    # rule parameter fields
    # When you add a field, update model test testCreation to check its defaulted to None
    # (Important for delegation to parent category)
    num_days_to_booking = models.IntegerField(null=True)
    can_make_recurring_booking = models.BooleanField(null=True)
    max_num_bookings = models.IntegerField(null=True)
    max_num_recurring_bookings = models.IntegerField(null=True)

    def get_parameter(self, param_name):
        value = getattr(self, param_name)

        if value is not None:
            return value

        value = self.parent_category.get_parameter(param_name)

        if value is None:
            raise Exception()

        return value

    def __str__(self):
        return self.name + " parent category: " + self.parent_category.name
