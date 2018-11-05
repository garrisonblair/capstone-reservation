from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.groups.serializers.group_serializer import GroupSerializer


class GroupView(APIView):

    def get(self, request):
        try:
            booker = request.user.booker
        except AttributeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        groups = booker.group_set.all()

        group_list = list()
        for group in groups:
            serializer = GroupSerializer(group)
            group_list.append(serializer.data)
        return Response(group_list, status=status.HTTP_200_OK)
