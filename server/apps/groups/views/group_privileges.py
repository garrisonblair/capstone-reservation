from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
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
        print(request_status)
        if request_status is not None:
            qs = qs.filter(status=request_status)

        return qs


class PrivilegeRequestCreate(APIView):
    permission_classes = (IsAuthenticated, IsBooker)

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
