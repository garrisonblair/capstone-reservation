import abc

from apps.util.ModelObserver import ModelObserver


# INTERFACE
class BookingExporter(ModelObserver, abc.ABC):

    @abc.abstractmethod
    def backup_booking(self, booking):
        pass
