import abc

from utils.ModelObserver import ModelObserver


# INTERFACE
class BookingExporter(ModelObserver, abc.ABC):

    @abc.abstractmethod
    def backup_booking(self, booking):
        pass
