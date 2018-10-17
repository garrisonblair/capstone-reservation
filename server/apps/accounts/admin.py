from django.contrib import admin
from .models.Student import Student
from .models.VerificationToken import VerificationToken


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'student_id', 'user', 'email', 'first_name', 'last_name')

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


admin.site.register(Student, StudentAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
