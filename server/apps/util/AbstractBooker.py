import abc


class AbstractBooker:

    @abc.abstractmethod
    def get_privileges(self):
        pass
