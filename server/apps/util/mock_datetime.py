# mock_datetime.py from https://solidgeargroup.com/mocking-the-time
import datetime
from unittest import mock
import functools

real_datetime_class = datetime.datetime


def mock_datetime(target, datetime_module):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

        @classmethod
        def today(cls):
            return target
    # Python2 & Python3-compatible metaclass
    mocked_datetime = DatetimeSubclassMeta('datetime', (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, 'datetime', mocked_datetime)


def datetime_mock(date_time):
    def decorator_datetime_mock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with mock_datetime(date_time, datetime):
                func(args[0])

        return wrapper
    return decorator_datetime_mock
