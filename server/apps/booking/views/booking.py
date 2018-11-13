import datetime
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.accounts.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from apps.accounts.permissions.IsBooker import IsBooker
from apps.booking.models.Booking import Booking
from apps.booking.serializers.booking_serializer import BookingSerializer, ReadBookingSerializer
from apps.accounts.exceptions import PrivilegeError


class BookingList(ListAPIView):
    permission_classes = ()
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        qs = super(BookingList, self).get_queryset()

        # Filter by year
        year = self.request.GET.get('year')
        if year:
            qs = Booking.objects.filter(date__year=year)

        # Filter by month
        month = self.request.GET.get('month')
        if month:
            qs = Booking.objects.filter(date__month=month)

        # Filter by day
        day = self.request.GET.get('day')
        if day:
            qs = Booking.objects.filter(date__day=day)

        return qs


class BookingCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = BookingSerializer

    def post(self, request):
        data = request.data
        data["booker"] = request.user.booker.booker_id

        serializer = BookingSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, PrivilegeError) as error:
            return Response(error.message, status=status.HTTP_400_BAD_REQUEST)


class BookingRetrieveUpdateDestroy(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, IsBooker)
    serializer_class = BookingSerializer

    def patch(self, request, pk):

        booking = Booking.objects.get(pk=pk)

        # Check permissions
        self.check_object_permissions(request, booking.booker.user)

        data = request.data
        data["booker"] = request.user.booker.booker_id
        serializer = BookingSerializer(booking, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
