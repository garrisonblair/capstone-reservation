import abc


class AbstractPrivilege:

    @abc.abstractmethod
    def get_parameter(self, param_name):
        pass

    @abc.abstractmethod
    def get_error_text(self, param_name):
        pass
