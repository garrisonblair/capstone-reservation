from rest_framework import serializers

from ..models.RecurringBooking import RecurringBooking, RecurringBookingSerializer
from apps.rooms.models.Room import Room
from apps.groups.models.Group import Group
from apps.accounts.models.Booker import Booker
