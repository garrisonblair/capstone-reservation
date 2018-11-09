from unittest import TestCase
from datetime import time

from ..comparators import *


class TestComparators(TestCase):

    def testBooleanComparatorTrueIsBetter(self):
        comparator = BooleanComparator()

        self.assertGreater(comparator.compare(True, False), 0)
        self.assertLess(comparator.compare(False, True), 0)

    def testBooleanComparatorFalseIsBetter(self):
        comparator = BooleanComparator(true_better=False)

        self.assertGreater(comparator.compare(False, True), 0)
        self.assertLess(comparator.compare(True, False), 0)

    def testIntegerComparatorBiggerIsBetter(self):
        comparator = IntegerComparator()

        self.assertGreater(comparator.compare(4, 3), 0)
        self.assertLess(comparator.compare(3, 4), 0)

    def testIntegerComparatorSmallerIsBetter(self):
        comparator = IntegerComparator(bigger_better=False)

        self.assertGreater(comparator.compare(3, 4), 0)
        self.assertLess(comparator.compare(4, 3), 0)

    def testTimeComparatorEarlierIsBetter(self):
        comparator = TimeComparator(earlier_better=True)

        self.assertLess(comparator.compare(time(12, 0, 0), time(11, 59, 59)), 0)
        self.assertGreater(comparator.compare(time(11, 59, 59), time(12, 0, 0)), 0)

    def testTimeComparatorLaterIsBetter(self):
        comparator = TimeComparator(earlier_better=False)

        self.assertGreater(comparator.compare(time(12, 0, 0), time(11, 59, 59)), 0)
        self.assertLess(comparator.compare(time(11, 59, 59), time(12, 0, 0)), 0)
