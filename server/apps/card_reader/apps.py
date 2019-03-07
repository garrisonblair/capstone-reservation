from django.apps.config import AppConfig


class CardReaderConfig(AppConfig):
    name = 'apps.card_reader'

    def __init__(self, arg1, arg2):
        super(CardReaderConfig, self).__init__(arg1, arg2)
        self.campon_listener = None

    def ready(self):
        from apps.booking.models.CampOn import CampOn
        from .CamponCreateListener import CamponCreateListener

        self.campon_listener = CamponCreateListener()
        CampOn().register(self.campon_listener)
