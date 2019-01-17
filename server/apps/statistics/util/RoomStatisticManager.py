import datetime


class RoomStatisticManager:

    def get_num_room_bookings(self, room, start_date=None, end_date=None):
        return room.get_bookings(start_date, end_date).count()

    def get_time_booked(self, room, start_date=None, end_date=None):
        time_booked = datetime.timedelta(hours=0)
        for booking in room.get_bookings(start_date, end_date).all():
            time_booked = time_booked + booking.get_duration()
        return time_booked
