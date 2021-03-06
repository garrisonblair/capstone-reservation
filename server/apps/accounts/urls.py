from django.urls import path
from apps.accounts.views.register import RegisterView
from apps.accounts.views.reset_password import ResetPasswordView
from apps.accounts.views.verify import VerifyView
from apps.accounts.views.login import LoginView
from apps.accounts.views.logout import LogoutView
from apps.accounts.views.user import UserList, UserRetrieveUpdate, BookerList
from apps.accounts.views.me import MyPrivileges, MyRecurringBookingPrivileges
from apps.accounts.views.privilege_categories import PrivilegeCategoryList
from apps.accounts.views.privilege_categories import PrivilegeCategoryCreate
from apps.accounts.views.privilege_categories import PrivilegeCategoryRetrieveUpdateDestroy
from apps.accounts.views.assign_privileges import PrivilegeCategoriesAssignSingleAutomatic
from apps.accounts.views.assign_privileges import PrivilegeCategoriesAssignAllAutomatic
from apps.accounts.views.assign_privileges import PrivilegeCategoriesAssignManual
from apps.accounts.views.assign_privileges import PrivilegeCategoriesRemoveManual

urlpatterns = [
    path(r'register', RegisterView.as_view()),
    path(r'reset_password', ResetPasswordView.as_view()),
    path(r'verify', VerifyView.as_view()),
    path(r'login', LoginView.as_view()),
    path(r'logout', LogoutView.as_view()),

    path(r'users', UserList.as_view()),
    path(r'user/<int:pk>', UserRetrieveUpdate.as_view()),
    path(r'bookers', BookerList.as_view()),

    path(r'my_privileges', MyPrivileges.as_view()),
    path(r'can_make_recurring', MyRecurringBookingPrivileges.as_view()),

    path(r'privilege_categories', PrivilegeCategoryList.as_view()),
    path(r'privilege_category', PrivilegeCategoryCreate.as_view()),
    path(r'privilege_category/<int:pk>', PrivilegeCategoryRetrieveUpdateDestroy.as_view()),

    path(r'assign_privileges', PrivilegeCategoriesAssignAllAutomatic.as_view()),
    path(r'assign_privileges/<int:pk>', PrivilegeCategoriesAssignSingleAutomatic.as_view()),
    path(r'assign_privilege', PrivilegeCategoriesAssignManual.as_view()),
    path(r'remove_privilege', PrivilegeCategoriesRemoveManual.as_view())
]
