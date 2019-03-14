import datetime
import decimal

from apps.booking.models.Booking import Booking
from apps.accounts.models.BookerProfile import BookerProfile
from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
import pdb


class ProgramStatisticManager:
    def get_program_bookings(self, program=None, grad_level=None, start_date=None, end_date=None):
        bookings = Booking.objects.all()
        if start_date is not None:
            bookings = bookings.filter(date__gte=start_date)
        if end_date is not None:
            bookings = bookings.filter(date__lte=end_date)
        if program is not None:
            program_bookers = BookerProfile.objects.filter(program=program)
            users = User.objects.filter(id__in=program_bookers)
            bookings = bookings.filter(booker_id__in=users)
        if grad_level is not None:
            grad_level_bookers = BookerProfile.objects.filter(graduate_level=grad_level)
            users = User.objects.filter(id__in=grad_level_bookers)
            bookings = bookings.filter(booker_id__in=users)

        return bookings

    def get_category_bookings(self, category):
        categories = PrivilegeCategory.objects.filter(name=category)
        category_bookers = BookerProfile.objects.filter(privilege_categories__in=categories)
        users = User.objects.filter(id__in=category_bookers)
        return Booking.objects.filter(booker_id__in=users)

    def get_num_program_bookings(self, program=None, grad_level=None, start_date=None, end_date=None):
        return self.get_program_bookings(program, grad_level, start_date, end_date).count()

    def get_num_category_bookings(self, category):
        return self.get_category_bookings(category).count()

    def get_program_time_booked(self, program=None, grad_level=None, start_date=None, end_date=None):
        time_booked = datetime.timedelta(hours=0)
        for booking in self.get_program_bookings(program, grad_level, start_date, end_date).all():
            time_booked = time_booked + booking.get_duration()
        return time_booked

    def get_category_time_booked(self, category):
        time_booked = datetime.timedelta(hours=0)
        for booking in self.get_category_bookings(category).all():
            time_booked = time_booked + booking.get_duration()
        return time_booked

    def get_average_bookings_per_day(self, program=None, grad_level=None,
                                     start_date=None,
                                     end_date=datetime.datetime.now().date()):
        if start_date is None:
            start_date = Booking.objects.get_first_booking_date()

        total_days = end_date - start_date
        total_days = total_days.days + 1
        decimal.getcontext().prec = 3
        num_room_bookings = self.get_num_program_bookings(program, grad_level, start_date, end_date)
        return float(decimal.Decimal(num_room_bookings) / decimal.Decimal(total_days))

    def get_average_time_booked_per_day(self, program=None, grad_level=None,
                                        start_date=None,
                                        end_date=datetime.datetime.now().date()):
        if start_date is None:
            start_date = Booking.objects.get_first_booking_date()

        total_days = end_date - start_date
        total_days = total_days.days + 1
        decimal.getcontext().prec = 3
        time_booked = self.get_program_time_booked(program, grad_level, start_date, end_date).total_seconds() / 3600
        return float(decimal.Decimal(time_booked) / decimal.Decimal(total_days))

    def get_program_serialized_statistics(self, program=None, grad_level=None, start_date=None, end_date=None):
        stats = dict()
        stats["program"] = program
        stats["grad_level"] = grad_level
        stats["num_bookings"] = self.get_num_program_bookings(program, grad_level, start_date, end_date)
        stats["hours_booked"] = self.get_program_time_booked(program, grad_level, start_date,
                                                             end_date).total_seconds() / 3600

        stats["average_bookings_per_day"] = self.get_average_bookings_per_day(program, grad_level, start_date, end_date)
        stats["average_time_booked_per_day"] = self.get_average_time_booked_per_day(
            program, grad_level, start_date, end_date)
        return stats

    def get_category_serialized_statistics(self, category):
        stats = dict()
        stats["category"] = category
        stats["num_bookings"] = self.get_num_category_bookings(category)
        stats["hours_booked"] = self.get_category_time_booked(category).total_seconds() / 3600

    def get_programs(self):
        return BookerProfile.objects.exclude(program__isnull=True).values('program').distinct()

    def get_grad_levels(self):
        return BookerProfile.objects.exclude(program__isnull=True).values('graduate_level').distinct()

    def get_categories(self):
        return PrivilegeCategory.objects.values('name').distinct()

    def get_all_statistics(self, with_program, with_grad_level, with_categories, start_date=None, end_date=None):
        all_stats = list()

        if with_program and with_grad_level:
            programs = self.get_programs()
            grad_levels = self.get_grad_levels()
            for program in programs:
                for grad_level in grad_levels:
                    all_stats.append(self.get_program_serialized_statistics(program['program'],
                                                                            grad_level['graduate_level'],
                                                                            start_date,
                                                                            end_date))
        elif with_program:
            programs = self.get_programs()
            for program in programs:
                all_stats.append(self.get_program_serialized_statistics(program['program'],
                                                                        None,
                                                                        start_date,
                                                                        end_date))

        elif with_grad_level:
            grad_levels = self.get_grad_levels()
            for grad_level in grad_levels:
                all_stats.append(self.get_program_serialized_statistics(None,
                                                                        grad_level['graduate_level'],
                                                                        start_date,
                                                                        end_date))

        if with_categories:
            categories = self.get_categories()
            for category in categories:
                all_stats.append(self.get_category_serialized_statistics(category["name"]))

        return all_stats
