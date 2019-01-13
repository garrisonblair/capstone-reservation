import abc
import datetime

from django.db.models import Q


class AbstractBooker:

    @abc.abstractmethod
    def get_privileges(self):
        pass

    @abc.abstractmethod
    def get_bookings(self):
        pass

    def get_non_recurring_bookings(self):
        return self.get_bookings().filter(recurring_booking=None)

    def get_active_non_recurring_bookings(self):
        today = datetime.datetime.now().date()
        now = datetime.datetime.now().time()

        return self.get_non_recurring_bookings().filter(Q(Q(date=today) & Q(end_time__gte=now))
                                                        | Q(date__gt=today))

    def get_non_recurring_bookings_for_date(self, date):
        return self.get_non_recurring_bookings().filter(date=date)

    def get_days_with_active_bookings(self):
        return self.get_active_non_recurring_bookings().values('date').distinct()
