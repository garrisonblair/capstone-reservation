from django.urls import path
from .views.user import UserList
from .views.me import MyUser
from rest_framework.authtoken import views


urlpatterns = [
    path(r'users', UserList.as_view()),
    path(r'login', views.obtain_auth_token),
    path(r'me', MyUser.as_view())
]
