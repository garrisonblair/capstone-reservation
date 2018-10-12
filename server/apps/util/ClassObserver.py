import abc

# INTERFACE
class ClassObserver(abc.ABC):

    @abc.abstractmethod
    def subject_saved(self, subject):
        pass

    @abc.abstractmethod
    def subject_updated(self, subject):
        pass

    @abc.abstractmethod
    def subject_deleted(self, subject):
        pass