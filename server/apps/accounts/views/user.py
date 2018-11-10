from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.Booker import Booker
from apps.accounts.serializers.UserSerializer import UserSerializer, UserSerializerLogin, BookerSerializer
from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializerLogin


class UserUpdate(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

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
        booker_id = request.data.get('booker_id')

        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permissions
        self.check_object_permissions(request, user)

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email

        if password:
            user.password = make_password(password)  # Hash password

        student = None
        if booker_id:
            try:
                student = Booker.objects.get(user=user)
                # Restrict student from changing its student ID once it's set
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            except Booker.DoesNotExist:
                # Add student ID only if it's a new user
                student = Booker(user=user, booker_id=booker_id)
                student.save()

        # Must be superuser to update those fields
        if username and request.user.is_superuser:
            user.username = username

        if is_active is not None and request.user.is_superuser:
            user.is_active = bool(is_active)

        if is_staff is not None and request.user.is_superuser:
            user.is_staff = bool(is_staff)

        if is_superuser is not None and request.user.is_superuser:
            user.is_superuser = bool(is_superuser)

        user.save()
        serializer = UserSerializer(user)
        if student:
            serializer = BookerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
