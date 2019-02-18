from rest_framework import serializers
from apps.card_reader.models.card_reader import CardReader

from apps.rooms.serializers.room import RoomSerializer


class ReadCardReaderSerializer(serializers.ModelSerializer):

    room = RoomSerializer(required=False)

    class Meta:
        model = CardReader
        fields = '__all__'


class WriteCardReaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardReader
        fields = '__all__'
