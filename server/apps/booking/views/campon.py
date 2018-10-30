from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.booking.serializers.campon_serializer import CampOnSerializer
from apps.booking.serializers.booking_serializer import BookingSerializer
import datetime


class CampOnView(APIView):

    def post(self, request):

        # Must be logged in as student
        if not request.user or not request.user.student:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        camp_on_data = dict(request.data)
        camp_on_data["student"] = request.user.student.student_id
        camp_on_data["start_time"] = datetime.datetime.now().now().replace(microsecond=0).time()
        serializer = CampOnSerializer(data=camp_on_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:

            current_booking = Booking.objects.get(id=camp_on_data["camped_on_booking"])
            request_end_time = datetime.datetime.strptime(camp_on_data["end_time"], "%H:%M").time()

            if request_end_time > current_booking.end_time:

                found_bookings = Booking.objects.filter(
                                    start_time__range=(current_booking.end_time, request_end_time))

                if found_bookings:
                    return Response("End time overlaps with future booking", status=status.HTTP_409_CONFLICT)
                # No Booking found, create new Booking and create CampOn

                camp_on_data["end_time"] = current_booking.end_time
                new_camp_on_serializer = CampOnSerializer(data=camp_on_data)

                if not new_camp_on_serializer.is_valid():
                    return Response(new_camp_on_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                camp_on = new_camp_on_serializer.save()

                new_booking = Booking(student=camp_on.student,
                                      student_group=camp_on.camped_on_booking.student_group,
                                      room=camp_on.camped_on_booking.room,
                                      date=camp_on.camped_on_booking.date,
                                      start_time=camp_on.end_time,
                                      end_time=request_end_time)

                new_booking.save()
                camp_on.generated_booking = new_booking

                response_data = {"CampOn": CampOnSerializer(camp_on).data,
                                 "Booking": BookingSerializer(new_booking).data}
                return Response(response_data, status=status.HTTP_201_CREATED)

            camp_on = serializer.save()
            return Response({"CampOn": CampOnSerializer(camp_on).data}, status=status.HTTP_201_CREATED)

        except (ValueError, ValidationError) as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        request_id = request.GET.get('id')
        request_booking = request.GET.get('camped_on_booking')
        request_start_time = request.GET.get('start_time')
        request_end_time = request.GET.get('end_time')

        try:
            if request_id is not None:
                camp_ons = CampOn.objects.filter(id=request_id)
            elif not(not request_booking or not request_start_time or not request_end_time):
                camp_ons = CampOn.objects.filter(camped_on_booking=request_booking,
                                                 start_time=request_start_time,
                                                 end_time=request_end_time)
            elif not(not request_start_time or not request_end_time):
                camp_ons = CampOn.objects.filter(start_time=request_start_time, end_time=request_end_time)
            elif request_booking is not None:
                camp_ons = CampOn.objects.filter(camped_on_booking=request_booking)
            else:
                camp_ons = CampOn.objects.all()
        except (ValueError, ValidationError) as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        camp_on_list = list()
        for camp_on in camp_ons:
            serializer = CampOnSerializer(camp_on)
            camp_on_list.append(serializer.data)
        return Response(camp_on_list, status=status.HTTP_200_OK)
