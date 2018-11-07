import abc
from datetime import datetime, date, timedelta


class AbstractComparator:

    # if value1 better return > 0, if value2 better, return < 0
    @abc.abstractmethod
    def compare(self, value1, value2):
        pass


class TimeComparator(AbstractComparator):

    def __init__(self, earlier_better):
        self.earlier_better = earlier_better

    def compare(self, value1, value2):
        value1 = datetime.combine(date.today(), value1)
        value2 = datetime.combine(date.today(), value2)

        if value1 == value2:
            return 1

        if self.earlier_better:
            difference = value1 - value2  # type: timedelta
            return difference.total_seconds()
        else:
            difference = value2 - value1
            return difference.total_seconds()


class IntegerComparator(AbstractComparator):

    def __init__(self, bigger_better=True):
        self.bigger_better = bigger_better

    def compare(self, value1, value2):
        if value1 == value2:
            return 1

        if self.bigger_better:
            return value1 - value2
        else:
            return value2 - value1


class BooleanComparator(AbstractComparator):

    def __init__(self, true_better=True):
        self.true_better = true_better

    def compare(self, value1, value2):
        if self.true_better:
            if value1:
                return 1
            else:
                return -1
        else:
            if not value1:
                return 1
            else:
                return -1
