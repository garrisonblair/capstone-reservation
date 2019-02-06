from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import PrivilegeCategory
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.permissions.IsBooker import IsBooker
from apps.accounts.models.User import User
from apps.groups.models.Group import Group
from apps.groups.serializers.privilege_request import WritePrivilegeRequestSerializer, ReadPrivilegeRequestSerializer
from apps.groups.models.PrivilegeRequest import PrivilegeRequest


class PrivilegeRequestList(ListAPIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = WritePrivilegeRequestSerializer
    queryset = PrivilegeRequest.objects.all()

    def get_queryset(self):
        qs = super(PrivilegeRequestList, self).get_queryset()

        if not self.request.user.is_superuser:
            try:
                owner = User.objects.get(id=self.request.user.id)
                owned_groups = owner.owned_groups.all()
                qs = qs.filter(group__in=owned_groups)
            except User.DoesNotExist:
                pass

        request_status = self.request.GET.get('status')
        if request_status is not None:
            qs = qs.filter(status=request_status)
        return qs


class PrivilegeRequestCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)
    serializer_class = ReadPrivilegeRequestSerializer

    def post(self, request):
        data = dict(request.data)

        group_id = data["group"]

        user = User.objects.get(id=request.user.id)

        if not user.owned_groups.filter(id=group_id).exists():
            return Response("User does not own this group", status=status.HTTP_400_BAD_REQUEST)

        serializer = ReadPrivilegeRequestSerializer(data=data)

        group = Group.objects.get(id=group_id)
        try:
            old_request = group.privilegerequest
            group.privilegerequest.delete()
        except PrivilegeRequest.DoesNotExist:
            pass

        if not serializer.is_valid():
            group.privilegerequest = old_request
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            privilege_request = serializer.save()
            serializer = WritePrivilegeRequestSerializer(privilege_request)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            group.privilegerequest = old_request
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)


class PrivilegeRequestDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def delete(self, request, pk, *args, **kwargs):
        user = User.cast_django_user(request.user)
        try:
            request = PrivilegeRequest.objects.get(id=pk)
        except PrivilegeRequest.DoesNotExist:
            return Response("Request does not exist", status=status.HTTP_400_BAD_REQUEST)

        if not request.group.owner_id == user.id:
            return Response("You do not have authorization to delete this request", status=status.HTTP_401_UNAUTHORIZED)

        request.delete()
        return Response("Request deleted", status=status.HTTP_200_OK)


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

        group.owner.send_email(subject, message)

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

        group.owner.send_email(subject, message)

        return Response("Request Denied", status=status.HTTP_200_OK)


class MyGroupPrivileges(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

    def get(self, request):
        user = User.cast_django_user(request.user)

        privileges = dict()

        for group in user.group_set.all():

            privilege_merger = group.get_privileges()
            group_privileges = dict()

            for field_name in PrivilegeCategory.get_parameter_names():
                if group.privilege_category is None:
                    group_privileges[field_name] = ''
                else:
                    group_privileges[field_name] = privilege_merger.get_parameter(field_name)

            privileges[group.name] = group_privileges

        return Response(privileges, status=status.HTTP_200_OK)
