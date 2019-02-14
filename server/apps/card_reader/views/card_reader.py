from rest_framework.views import View

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.accounts.permissions.IsSuperUser import IsSuperUser
from apps.card_reader.models.card_reader import CardReader
from apps.card_reader.serializers.card_reader import ReadCardReaderSerializer, WriteCardReaderSerializer


class ListCardReaders(ListAPIView):

    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = ReadCardReaderSerializer

    def get_queryset(self):

        qs = CardReader.objects.all()

        room = self.request.GET.get('room')
        if room:
            qs = qs.filter(room=room)

        return qs


class CardReaderCreateView(CreateAPIView):

    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer


class CardReaderUpdateView(UpdateAPIView):
    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer


class CardReaderDeleteView(DestroyAPIView):

    queryset = CardReader.objects.all()
    permission_classes = (IsSuperUser,)
    serializer_class = WriteCardReaderSerializer
