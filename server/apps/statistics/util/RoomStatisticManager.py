import datetime
import decimal

from apps.booking.models import Booking


class RoomStatisticManager:
    def get_num_room_bookings(self, room, start_date=None, end_date=None):
        return room.get_bookings(start_date, end_date).count()

    def get_time_booked(self, room, start_date=None, end_date=None):
        time_booked = datetime.timedelta(hours=0)
        for booking in room.get_bookings(start_date, end_date).all():
            time_booked = time_booked + booking.get_duration()
        return time_booked

    def get_average_bookings_per_day(self, room,
                                     start_date=Booking.get_first_booking_date(),
                                     end_date=datetime.datetime.now().date()):
        total_days = end_date - start_date
        total_days = total_days.days + 1
        decimal.getcontext().prec = 3
        num_room_bookings = self.get_num_room_bookings(room=room, start_date=start_date, end_date=end_date)
        return float(decimal.Decimal(num_room_bookings) / decimal.Decimal(total_days))
