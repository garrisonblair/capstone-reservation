from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions.IsBooker import IsBooker
from ..models.BookerProfile import BookerProfile
from ..serializers.user import UserSerializer, BookerSerializer
from ..permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from ..permissions.IsSuperUser import IsSuperUser
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        search_term = self.request.query_params.get("search_text")
        users = User.objects.all()

        if search_term is not None:
            users = users.filter(Q(username__contains=search_term) |
                                 Q(first_name__contains=search_term) |
                                 Q(last_name__contains=search_term))

        return users


class BookerList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    queryset = BookerProfile.objects.all()
    serializer_class = BookerSerializer

    def get_queryset(self):
        search_term = self.request.GET.get("search_text")
        qs = super(BookerList, self).get_queryset()

        if search_term is not None:
            qs = qs.filter(Q(user__username__contains=search_term) |
                           Q(user__first_name__contains=search_term) |
                           Q(user__last_name__contains=search_term))

        return qs


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

        booker = BookerProfile.objects.get(user_id=user.id)
        # Add booker ID only if it's a new user
        booker.booker_id = booker_id
        booker.save()
        # Add Booker Privileges
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(user.bookerprofile)

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
