import abc

from apps.util.ClassObserver import ClassObserver


# INTERFACE
class BookingExporter(ClassObserver, abc.ABC):

    @abc.abstractmethod
    def backup_booking(self, booking):
        pass
