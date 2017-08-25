from unittest import TestCase
from sqlite3 import connect, PARSE_DECLTYPES
from datetime import date
from employees import Employees


class TestEmployees(TestCase):
    def setUp(self):
        connection = connect(':memory:', detect_types=PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE employees
                            (first TEXT,
                            last TEXT,
                            date_of_employment DATE)''')
        cursor.execute('''INSERT INTO employees
                            (first, last, date_of_employment)
                          VALUES
                            ("Test1", "Employee", :date)''', {'date': date(year=2003, month=7, day=12)})
        cursor.execute('''INSERT INTO employees
                            (first, last, date_of_employment)
                          VALUES
                            ("Test2", "Employee", :date)''', {'date': date(year=2001, month=3, day=18)})
        cursor.execute('''INSERT INTO employees
                            (first, last, date_of_employment)
                          VALUES
                            ("Test3", "Employee", :date)''', {'date': date.today()})
        self.connection = connection

    def tearDown(self):
        self.connection.close()

    def test_add_employee(self):
        to_test = Employees(self.connection)
        to_test.add_employee('Test1', 'Employee', date.today())
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM employees
                          ORDER BY date_of_employment''')
        self.assertEqual(tuple(cursor), (('Test2', 'Employee', date(2001, 3, 18)),
                                         ('Test1', 'Employee', date(2003, 7, 12)),
                                         ('Test3', 'Employee', date.today()),
                                         ('Test1', 'Employee', date.today())))

    def test_find_employees_by_name(self):
        to_test = Employees(self.connection)
        found = tuple(to_test.find_employees_by_name('Test1','employee'))
        expected = (('Test1','Employee',date(2003,7,12)),)
        self.assertEqual(found,expected)

    def test_find_employees_by_date(self):
        to_test = Employees(self.connection)
        target = date.today()
        found = tuple(to_test.find_employees_by_date(target),)
        expected = (('Test3','Employee',date.today()),)
        self.assertEqual(found,expected)
