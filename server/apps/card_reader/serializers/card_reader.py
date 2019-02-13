from rest_framework import serializers
from apps.card_reader.models.card_reader import CardReader

from apps.rooms.serializers.room import RoomSerializer


class CardReaderSerializer(serializers.ModelSerializer):

    room = serializers.SerializerMethodField()

    class Meta:
        model = CardReader
        fields = '__all__'

    def get_room(self, card_reader):
        if card_reader.room:
            return RoomSerializer(card_reader.room).data
        return None
