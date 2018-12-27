from django.contrib import admin
from .models.Booker import Booker
from .models.VerificationToken import VerificationToken
from .models.PrivilegeCategory import PrivilegeCategory


class BookerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'booker_id', 'user', 'email', 'first_name', 'last_name')

    def user_id(self, instance):
        return instance.user.id

    def first_name(self, instance):
        return instance.user.first_name

    def last_name(self, instance):
        return instance.user.last_name

    def email(self, instance):
        return instance.user.email


class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'token', 'expiration')

    def user_id(self, instance):
        return instance.user.id

    def email(self, instance):
        return instance.user.email


class PrivilegeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'parent_category',
                    'max_days_until_booking',
                    'can_make_recurring_booking',
                    'max_overall_bookings',
                    'max_daily_bookings',
                    'max_recurring_bookings',
                    'booking_start_time',
                    'booking_end_time'
                    )


admin.site.register(Booker, BookerAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
admin.site.register(PrivilegeCategory, PrivilegeCategoryAdmin)
