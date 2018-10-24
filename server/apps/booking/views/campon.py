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


