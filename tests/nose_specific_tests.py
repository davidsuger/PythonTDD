import sys
from sqlite3 import connect
from imp import reload


class grouped_tests:
    def setup(self):
        self.connection = connect(':memory:')
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE test (a, b, c)')
        cursor.execute('''INSERT INTO test (a, b, c) VALUES (1, 2, 3)''')
        self.connection.commit()

    def teardown(self):
        self.connection.close()

    def test_update(self):
        cursor = self.connection.cursor()
        cursor.execute('UPDATE test SET b = 7 WHERE a = 1')

    def test_select(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM test LIMIT 1')
        assert cursor.fetchone() == (1, 2, 3)


def platform_setup():
    sys.platform = 'test platform'


def platform_teardown():
    global sys
    sys = reload(sys)


def standalone_test():
    assert sys.platform == 'test platform'


standalone_test.setup = platform_setup
standalone_test.teardown = platform_teardown
