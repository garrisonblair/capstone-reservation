from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.Booker import Booker
from ..serializers.user import UserSerializer, BookerSerializer
from ..permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from ..permissions.IsSuperUser import IsSuperUser
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        search_term = self.request.GET.get("search_text")
        print(search_term)
        users = User.objects.all()

        if search_term is not None:
            users = users.filter(Q(username__contains=search_term) |
                                 Q(first_name__contains=search_term) |
                                 Q(last_name__contains=search_term))

        return users


class UserUpdate(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def patch(self, request, pk):
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

        booker = None
        if booker_id:
            try:
                booker = Booker.objects.get(user=user)
                # Restrict student from changing its student ID once it's set
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            except Booker.DoesNotExist:
                # Add booker ID only if it's a new user
                booker = Booker(user=user, booker_id=booker_id)
                booker.save()
                # Add Booker Privileges
                manager = PrivilegeCategoryManager()
                manager.assign_booker_privileges(user.booker)

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
        if booker:
            serializer = BookerSerializer(booker)
        return Response(serializer.data, status=status.HTTP_200_OK)
