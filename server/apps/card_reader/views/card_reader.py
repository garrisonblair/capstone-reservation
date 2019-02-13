from rest_framework.views import View

from rest_framework.generics import ListAPIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.card_reader.models.card_reader import CardReader
from apps.card_reader.serializers.card_reader import CardReaderSerializer


class ListCardReaders(ListAPIView):

    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = CardReaderSerializer
