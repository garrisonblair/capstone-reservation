from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.Booker import Booker
from apps.groups.serializers.privilege_request import WritePrivilegeRequestSerializer, ReadPrivilegeRequestSerializer
from apps.groups.models.PrivilegeRequest import PrivilegeRequest


class PrivilegeRequestList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadPrivilegeRequestSerializer
    queryset = PrivilegeRequest.objects.all()

    def get_queryset(self):
        qs = super(PrivilegeRequestList, self).get_queryset()
        try:
            owner = Booker.objects.get(booker_id=self.request.user.booker)
            owned_groups = owner.owned_groups.all()
            qs = qs.filter(group__in=owned_groups)
        except Booker.DoesNotExist:
            pass

        request_status = self.request.GET.get('status')
        if request_status == PrivilegeRequest.PE:
            qs = qs.filter(status=PrivilegeRequest.PE)
        elif request_status == PrivilegeRequest.DE:
            qs = qs.filter(status=PrivilegeRequest.DE)
        elif request_status == PrivilegeRequest.AP:
            qs = qs.filter(status=PrivilegeRequest.AP)

        return qs


class PrivilegeRequestCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadPrivilegeRequestSerializer

    def post(self, request):
        data = dict(request.data)

        serializer = ReadPrivilegeRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            privilege_request = serializer.save()
            serializer = WritePrivilegeRequestSerializer(privilege_request)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class PrivilegeRequestsList(ListAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser)
    serializer_class = ReadPrivilegeRequestSerializer
    queryset = PrivilegeRequest.objects.all()

    def get_queryset(self):
        qs = super(PrivilegeRequestsList, self).get_queryset()

        request_status = self.request.GET.get('status')
        if request_status == PrivilegeRequest.PE:
            qs = qs.filter(status=PrivilegeRequest.PE)
        elif request_status == PrivilegeRequest.DE:
            qs = qs.filter(status=PrivilegeRequest.DE)
        elif request_status == PrivilegeRequest.AP:
            qs = qs.filter(status=PrivilegeRequest.AP)

        return qs


class ApprovePrivilegeRequest(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        data = dict(request.data)
        pk = data['privilege_request']
        try:
            privilege_request = PrivilegeRequest.objects.get(id=pk)
        except PrivilegeRequest.DoesNotExist:
            return Response("Privilege Request does not exist", status=status.HTTP_400_BAD_REQUEST)

        group = privilege_request.group
        category = privilege_request.privilege_category
        group.privilege_category = category
        group.save()
        privilege_request.status = PrivilegeRequest.AP
        privilege_request.save()

        subject = "Group Booking Privilege Request Approval"
        message = "Your request for group privileges has been approved.\n" \
                  "\n" \
                  "Group: {}\n" \
                  "Privilege Category: {}\n" \
                  "\n" \
                  "You can view your booking privileges on your account".format(group.name, category.name)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [group.owner.user.email]
        )

        return Response("Request Approved", status=status.HTTP_200_OK)


class DenyPrivilegeRequest(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        data = dict(request.data)
        pk = data['privilege_request']
        try:
            privilege_request = PrivilegeRequest.objects.get(id=pk)
        except PrivilegeRequest.DoesNotExist:
            return Response("Privilege Request does not exist", status=status.HTTP_400_BAD_REQUEST)

        group = privilege_request.group
        category = privilege_request.privilege_category
        privilege_request.status = PrivilegeRequest.DE
        privilege_request.save()

        denial_reason = data['denial_reason']

        subject = "Group Booking Privilege Request Denied"
        message = "Your request for group privileges has been denied.\n" \
                  "\n" \
                  "Group: {}\n" \
                  "Privilege Category: {}\n" \
                  "\n" \
                  "Reason Provided: {}".format(group.name, category.name, denial_reason)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [group.owner.user.email]
        )

        return Response("Request Denied", status=status.HTTP_200_OK)
