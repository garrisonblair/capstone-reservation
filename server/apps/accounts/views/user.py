from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.serializers.UserSerializer import UserSerializer, UserSerializerLogin


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerLogin


# TODO: Update password
# TODO: Check permission
class UserUpdate(APIView):

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        is_active = request.data.get('is_active')
        is_staff = request.data.get('is_staff')
        is_superuser = request.data.get('is_superuser')

        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if username:
            user.username = username

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email

        # Must be superuser to update those fields
        if is_active is not None and request.user.is_superuser:
            user.is_active = bool(is_active)

        if is_staff is not None and request.user.is_superuser:
            user.is_staff = bool(is_staff)

        if is_superuser is not None and request.user.is_superuser:
            user.is_superuser = bool(is_superuser)

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

