from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models.Student import Student
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

        campon_data = dict(request.data)
        campon_data["student"] = request.user.student.student_id
        serializer = CampOnSerializer(data=campon_data)

        if serializer.is_valid():
            try:
                # If the CampOn end time is bigger than Booking end time, the system will check if there is Booking between the Booking end time and CampOn end time
                # If there is Booking, the system will create a CampOn with current time as start time and the specified end time as end time
                # Otherwise, the system will create a Booking and a CampOn for the student

                current_booking = Booking.objects.get(id=campon_data["booking"])
                request_end_time = datetime.datetime.strptime(campon_data["end_time"], "%H:%M").time()

                if request_end_time > current_booking.end_time:
                    found_booking = Booking.objects.filter(start_time__range=(current_booking.end_time, request_end_time))
                    if not found_booking: 

                        # No Booking found, create new Booking and create CampOn
                        new_booking_serializer = BookingSerializer(data={'student': request.user.student.student_id, 
                                                                         'room': current_booking.room.id, 
                                                                         'date': current_booking.date, 
                                                                         'start_time': current_booking.end_time, 
                                                                         'end_time': request_end_time})

                        campon_data["end_time"] = current_booking.end_time
                        new_campon_serializer = CampOnSerializer(data=campon_data)

                        if new_booking_serializer.is_valid() and new_campon_serializer.is_valid():
                            new_booking = new_booking_serializer.save()
                            new_campon = new_campon_serializer.save()
                            Serializer_list = [BookingSerializer(new_booking).data, CampOnSerializer(new_campon).data]
                            return Response(Serializer_list, status=status.HTTP_201_CREATED)

                campon = serializer.save()
                return Response(CampOnSerializer(campon).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            cmapons = CampOn.objects.all()
            camponsList = list()
            for campon in cmapons:
                serializer = CampOnSerializer(campon)
                camponsList.append(serializer.data)
            return Response(camponsList, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


