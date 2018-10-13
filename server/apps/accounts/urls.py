from django.urls import path
from apps.accounts.views.register import RegisterView
from apps.accounts.views.verify import VerifyView
from apps.accounts.views.login import LoginView
from apps.accounts.views.user import UserList
from apps.accounts.views.me import MyUser

urlpatterns = [
    path(r'register', RegisterView.as_view()),
    path(r'verify', VerifyView.as_view()),
    path(r'login', LoginView.as_view()),

    path(r'users', UserList.as_view()),
    path(r'me', MyUser.as_view())
]
