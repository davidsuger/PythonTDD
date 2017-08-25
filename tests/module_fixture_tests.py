from unittest import TestCase
from unittest.mock import patch,Mock
from datetime import date

fake_date=Mock()
fake_date.today=Mock(return_value=date(2014,6,12))
patch_date=patch('tests.module_fixture_tests.date',fake_date)

def setup():
    patch_date.start()

def teardown():
    patch_date.stop()

class first_tests(TestCase):
    def test_year(self):
        self.assertEqual(date.today().year,2014)

    def test_month(self):
        self.assertEqual(date.today().month,6)

    def test_year(self):
        self.assertEqual(date.today().day,12)

class second_tests(TestCase):
    def test_isoformat(self):
        self.assertEqual(date.today().isoformat(),'2014-06-12')