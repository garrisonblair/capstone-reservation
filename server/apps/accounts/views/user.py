from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from apps.accounts.serializers.UserSerializer import UserSerializerLogin


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerLogin
