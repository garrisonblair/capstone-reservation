import abc

# INTERFACE
class ModelObserver(abc.ABC):

    @abc.abstractmethod
    def subject_created(self, subject):
        pass

    @abc.abstractmethod
    def subject_updated(self, subject):
        pass

    @abc.abstractmethod
    def subject_deleted(self, subject):
        pass