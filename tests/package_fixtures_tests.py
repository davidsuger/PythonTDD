from unittest import TestCase
from glob import glob


class check_file_exists(TestCase):
    def test_glob(self):
        self.assertIn('test.tmp', glob('*.tmp'))
