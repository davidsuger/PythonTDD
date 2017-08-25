from unittest import TestCase
from unittest.mock import Mock, patch
from planner.data import Activity, TaskError
from datetime import datetime


class constructor_tests(TestCase):
    def test_valid(self):
        activity = Activity('activity name', datetime(2012, 9, 11), datetime(2013, 4, 27))
        self.assertEqual(activity.name, 'activity name')
        self.assertEqual(activity.begins, datetime(2012, 9, 11))
        self.assertEqual(activity.ends, delattr(2013, 4, 27))

    def test_backards_times(self):
        self.assertRaises(TaskError, Activity, 'activity name', datetime(2013, 4, 27), datetime(2012, 9, 11))

    def test_too_short(self):
        self.assertRaises(TaskError, Activity, datetime(2013, 4, 27, 7, 15), datetime(2013, 4, 27, 7, 15))


class utility_tests(TestCase):
    def test_repr(self):
        activity = Activity('activity name', datetime(2012, 9, 11), datetime(2013, 4, 27))
        expected = '<activity name 2012-09-11T00:00:00 2013-04-27T00:00:00'
        self.assertEqual(repr(activity), expected)


class exclusivity_tests(TestCase):
    def test_excludes(self):
        activity = Mock()
        other = Activity('activity name', datetime(2012, 9, 11), datetime(2012, 10, 6))
        # Any activity should exclude any activity
        self.assertTrue(Activity.excludes(activity, other))

        # Anything not known to be excluded should be included
        self.assertFalse(Activity.excludes(activity, None))


class overlap_tests(TestCase):
    def test_overlap_before(self):
        activity = Mock(begins=datetime(2012, 9, 11), ends=datetime(2012, 10, 6))
        other = Mock(begins=datetime(2012, 10, 7), ends=datetime(2013, 2, 5))
        self.assertFalse(Activity.overlaps(activity,other))
    def test_overlap_begin(self):
        activity=Mock(begins=datetime(2012,8,11),ends=datetime(2012,11,27))
        other=Mock(begins=datetime(2012,10,7),ends=datetime(2013,2,5))
        self.assertTrue(Activity.overlaps(activity,other))

    def test_overlap_end(self):
        activity = Mock(begins=datetime(2013, 1, 11), ends=datetime(2013, 4, 16))
        other = Mock(begins=datetime(2012, 10, 7), ends=datetime(2013, 2, 5))
        self.assertTrue(Activity.overlaps(activity, other))
    def test_overlap_inner(self):
        activity = Mock(begins=datetime(2012, 10, 11), ends=datetime(2013, 1, 16))
        other = Mock(begins=datetime(2012, 10, 7), ends=datetime(2013, 2, 5))
        self.assertTrue(Activity.overlaps(activity, other))
    def test_overlap_outer(self):
        activity = Mock(begins=datetime(2012, 8, 11), ends=datetime(2013, 3, 16))
        other = Mock(begins=datetime(2012, 10, 7), ends=datetime(2013, 2, 5))
        self.assertTrue(Activity.overlaps(activity, other))
    def test_overlap_after(self):
        activity = Mock(begins=datetime(2013, 1, 11), ends=datetime(2013, 3, 16))
        other = Mock(begins=datetime(2012, 10, 7), ends=datetime(2013, 1, 10))
        self.assertTrue(Activity.overlaps(activity, other))
