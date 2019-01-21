import datetime
import decimal

from apps.booking.models import Booking
from apps.rooms.serializers.room import RoomSerializer


class RoomStatisticManager:
    def get_first_booking_date(self):
        if Booking.objects.count() == 0:
            return datetime.datetime.now().date()
        return Booking.objects.order_by("date").first().date

    def get_num_room_bookings(self, room, start_date=None, end_date=None):
        return room.get_bookings(start_date, end_date).count()

    def get_time_booked(self, room, start_date=None, end_date=None):
        time_booked = datetime.timedelta(hours=0)
        for booking in room.get_bookings(start_date, end_date).all():
            time_booked = time_booked + booking.get_duration()
        return time_booked

    def get_average_bookings_per_day(self, room,
                                     start_date=None,
                                     end_date=datetime.datetime.now().date()):
        if start_date is None:
            start_date = self.get_first_booking_date()

        total_days = end_date - start_date
        total_days = total_days.days + 1
        decimal.getcontext().prec = 3
        num_room_bookings = self.get_num_room_bookings(room=room, start_date=start_date, end_date=end_date)
        return float(decimal.Decimal(num_room_bookings) / decimal.Decimal(total_days))

    def get_average_time_booked_per_day(self, room,
                                        start_date=None,
                                        end_date=datetime.datetime.now().date()):
        if start_date is None:
            start_date = self.get_first_booking_date()

        total_days = end_date - start_date
        total_days = total_days.days + 1
        decimal.getcontext().prec = 3
        time_booked = self.get_time_booked(room=room, start_date=start_date, end_date=end_date).total_seconds() / 3600
        return float(decimal.Decimal(time_booked) / decimal.Decimal(total_days))

    def get_serialized_statistics(self, room, start_date=None, end_date=None):
        stats = dict()
        stats["room"] = RoomSerializer(room).data
        stats["num_room_bookings"] = self.get_num_room_bookings(room, start_date, end_date)
        stats["hours_booked"] = self.get_time_booked(room, start_date, end_date).total_seconds() / 3600

        if start_date is None and end_date is None:
            stats["average_bookings_per_day"] = self.get_average_bookings_per_day(room)
            stats["average_time_booked_per_day"] = self.get_average_time_booked_per_day(room)
            return stats

        if start_date is None and end_date is not None:
            stats["average_bookings_per_day"] = self.get_average_bookings_per_day(room, end_date)
            stats["average_time_booked_per_day"] = self.get_average_time_booked_per_day(room, end_date)
            return stats

        if start_date is not None and end_date is None:
            stats["average_bookings_per_day"] = self.get_average_bookings_per_day(room, start_date)
            stats["average_time_booked_per_day"] = self.get_average_time_booked_per_day(room, start_date)
            return stats

        stats["average_bookings_per_day"] = self.get_average_bookings_per_day(room, start_date, end_date)
        stats["average_time_booked_per_day"] = self.get_average_time_booked_per_day(room, start_date, end_date)
        return stats
