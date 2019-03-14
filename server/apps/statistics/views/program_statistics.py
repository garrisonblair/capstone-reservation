import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.statistics.util.ProgramStatisticManager import ProgramStatisticManager


class ProgramStatistics(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def get(self, request):
        with_program = request.GET.getlist('with_program')
        with_grad_level = request.GET.getlist('with_grad_level')
        with_categories = request.GET.getlist('with_categories')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if start_date is not None:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date is not None:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        manager = ProgramStatisticManager()

        program_stats = manager.get_all_statistics(with_program, with_grad_level, with_categories, start_date, end_date)

        return Response(program_stats, status.HTTP_200_OK)
