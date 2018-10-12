from django.urls import path
from apps.accounts.views.user import UserList
from apps.accounts.views.me import MyUser
from apps.accounts.views.login import LoginView

urlpatterns = [
    path(r'users', UserList.as_view()),
    path(r'login', LoginView.as_view()),
    path(r'me', MyUser.as_view())
]
