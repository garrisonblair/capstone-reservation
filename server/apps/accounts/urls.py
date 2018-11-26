from django.urls import path
from apps.accounts.views.register import RegisterView
from apps.accounts.views.verify import VerifyView
from apps.accounts.views.login import LoginView
from apps.accounts.views.logout import LogoutView
from apps.accounts.views.user import UserList, UserUpdate
from apps.accounts.views.me import MyUser
from apps.accounts.views.privilege_categories import PrivilegeCategoryList
from apps.accounts.views.privilege_categories import PrivilegeCategoryCreate
from apps.accounts.views.privilege_categories import PrivilegeCategoryRetrieveUpdateDestroy

urlpatterns = [
    path(r'register', RegisterView.as_view()),
    path(r'verify', VerifyView.as_view()),
    path(r'login', LoginView.as_view()),
    path(r'logout', LogoutView.as_view()),

    path(r'users', UserList.as_view()),
    path(r'user/<int:pk>', UserUpdate.as_view()),
    path(r'me', MyUser.as_view()),

    path(r'privilege_categories', PrivilegeCategoryList.as_view()),
    path(r'privilege_category', PrivilegeCategoryCreate.as_view()),
    path(r'privilege_category/<int:pk>', PrivilegeCategoryRetrieveUpdateDestroy.as_view())
]
