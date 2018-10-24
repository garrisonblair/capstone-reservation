from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models.Student import Student
from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.booking.serializers.campon_serializer import CampOnSerializer

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
                current_booking = Booking.objects.get(id=request.booking)

                # If the CampOn end time is bigger than Booking end time, the system will check if there is Booking between the Booking end time and CampOn end time
                # If there is Booking, the system will create a CampOn with current time as start time and the specified end time as end time
                # Otherwise, the system will create a Booking and a CampOn for the student

                if request.end_time > current_booking.end_time:
                    resullt = Booking.objects.filter(start_time__range=(current_booking.end_time, request.end_time))
                    if len(result) > 0: 

                        # Found Booking, create CampOn
                        serializer = CampOnSerializer(data=campon_data)
                        campon = serializer.save()
                        return Response(CampOnSerializer(campon).data, status=status.HTTP_201_CREATED)
                    else:

                        # No Booking found, create booking
                        booking_serializer = BookingSerializer(data={'student': request.user.student.student_id, 
                                                                     'room': current_booking.room, 
                                                                     'date': current_booking.date, 
                                                                     'start_time': current_booking.end_time, 
                                                                     'end_time':request.end_time})
                        if booking_serializer.is_valid():
                            try:
                                booking = serializer.save()

                                # Edit CampOn end time, create CampOn
                                campon_data.end_time = current_booking.end_time
                                serializer = CampOnSerializer(data=campon_data)
                                booking = serializer.save()
                                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
                            except ValidationError as error:
                                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
                else:
                    campon = serializer.save()
                    return Response(CampOnSerializer(campon).data, status=status.HTTP_201_CREATED)
            except ValidationError as error:
                return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

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


