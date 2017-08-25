from unittest import TestCase
from unittest.mock import patch, Mock
from planner.data import Schedule, ScheduleError
from datetime import datetime


class add_tests(TestCase):
    overlap_exclude = Mock()
    overlap_exclude.overlaps = Mock(return_value=True)
    overlap_exclude.excludes = Mock(return_value=True)
    overlap_include = Mock()
    overlap_include.overlaps = Mock(return_value=True)
    overlap_include.excludes = Mock(return_value=False)
    distinct_exclude = Mock()
    distinct_exclude.overlaps = Mock(return_value=False)
    distinct_exclude.excludes = Mock(return_value=True)
    distinct_include = Mock()
    distinct_include.overlaps = Mock(return_value=False)
    distinct_include.excludes = Mock(return_value=False)

    def test_add_overlap_exclude(self):
        schedule = Schedule()
        schedule.add(self.distinct_include)
        self.assertRaises(ScheduleError, schedule.add, self.overlap_exclude)

    def test_add_overlap_include(self):
        schedule = Schedule()
        schedule.add(self.distinct_include)
        schedule.add(self.overlap_include)

    def test_add_distinct_exclude(self):
        schedule = Schedule()
        schedule.add(self.distinct_include)
        schedule.add(self.distinct_exclude)

    def test_add_distinct_include(self):
        schedule = Schedule()
        schedule.add(self.distinct_include)
        schedule.add(self.distinct_include)

    def test_add_over_overlap_exclude(self):
        schedule = Schedule()
        schedule.add(self.overlap_exclude)
        self.assertRaises(ScheduleError, schedule.add, self.overlap_include)

    def test_add_over_distinct_exclude(self):
        schedule = Schedule()
        schedule.add(self.distinct_exclude)
        self.assertRaises(ScheduleError, schedule.add, self.overlap_include)

    def test_add_over_overlap_include(self):
        schedule = Schedule()
        schedule.add(self.overlap_include)
        schedule.add(self.overlap_include)

    def test_add_over_distinct_include(self):
        schedule = Schedule()
        schedule.add(self.distinct_include)
        schedule.add(self.overlap_include)


class in_tests(TestCase):
    fake = Mock()
    fake.overlaps = Mock(return_value=True)
    fake.excludes = Mock(return_value=True)

    def test_in_before_add(self):
        schedule = Schedule()
        self.assertFalse(self.fake in schedule)

    def test_in_after_add(self):
        schedule = Schedule()
        schedule.add(self.fake)
        self.assertTrue(self.fake in schedule)
