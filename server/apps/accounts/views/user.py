from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from apps.util.AbstractPaginatedView import AbstractPaginatedView

from apps.accounts.permissions.IsBooker import IsBooker
from ..models.BookerProfile import BookerProfile
from ..serializers.user import UserSerializer, BookerProfileSerializer
from ..permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class UserList(ListAPIView, AbstractPaginatedView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        users = User.objects.all()
        keyword = self.request.query_params.get("keyword")
        is_superuser = self.request.query_params.get("is_superuser")
        is_staff = self.request.query_params.get("is_staff")
        is_active = self.request.query_params.get("is_active")

        if keyword is not None:
            users = users.filter(Q(username__contains=keyword) |
                                 Q(first_name__contains=keyword) |
                                 Q(last_name__contains=keyword) |
                                 Q(email__contains=keyword))

        if is_superuser is not None:
            users = users.filter(is_superuser=is_superuser)

        if is_staff is not None:
            users = users.filter(is_staff=is_staff)

        if is_active is not None:
            users = users.filter(is_active=is_active)

        return users

    def get(self, request):
        try:
            qs = self.get_queryset()
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = UserSerializer(qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BookerList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    queryset = BookerProfile.objects.all()
    serializer_class = BookerProfileSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get("search_text")
        qs = super(BookerList, self).get_queryset()

        if search_term is not None:
            qs = qs.filter(Q(user__username__contains=search_term) |
                           Q(user__first_name__contains=search_term) |
                           Q(user__last_name__contains=search_term))

        return qs


class UserRetrieveUpdate(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get(self, request, pk):
        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permissions
        self.check_object_permissions(request, user)
        return Response(UserSerializer(user).data)

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
        secondary_email = request.data.get('secondary_email')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

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

        if old_password and not user.check_password(old_password):
            print("WRONG OLD PASSWORD")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if old_password and new_password:
            user.password = make_password(new_password)

        booker = BookerProfile.objects.get(user_id=user.id)

        if booker_id:
            booker.booker_id = booker_id

        if secondary_email:
            booker.secondary_email = secondary_email

        booker.save()
        # Add Booker Privileges
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(user)

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

        return Response(serializer.data, status=status.HTTP_200_OK)
