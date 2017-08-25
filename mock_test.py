from unittest.mock import Mock, call
import itertools

mock = Mock()
print(mock)
print(mock.x)
print(mock.x)
print(mock.x('Foo', 3, 14))
print(mock.x('Foo', 3, 14))
print(mock.x('Foo', 99, 12))
print(mock.y(mock.x('Foo', 1, 1)))

print(mock.method_calls)

mock.assert_has_calls([call.x('Foo', 1, 1)])
mock.assert_has_calls([call.x('Foo', 3, 14), call.x('Foo', 99, 12)])
mock.assert_has_calls([call.x('Foo', 1, 1), call.x('Foo', 99, 12)], any_order=True)
# mock.assert_has_calls([call.x('Foo', 1, 1), call.x('Foo', 99, 12)])

mock.assert_has_calls([call.y(mock.x.return_value)])

print(mock.x('Foo', 99, 12).return_value)

print(mock.z.hello(23).stuff.howdy('a', 'b', 'c'))
mock.assert_has_calls([call.z.hello().stuff.howdy('a', 'b', 'c')])

print(mock.method_calls)
print(mock.mock_calls.index(call.z.hello(23)))

print(mock.mock_calls.index(call.z.hello().stuff.howdy('a', 'b', 'c')))

mock.q = 5
print(mock.q)

mock.o.return_value = 'Hi'
print(mock.o())
print(mock.o('Howdy'))

mock.p.side_effect = [1, 2, 3]
print(mock.p())
print(mock.p())
print(mock.p())

# mock.p.side_effect = itertools.count()
# while True:
#     print(mock.p())

mock.e.side_effect = [1, ValueError('x')]
print(mock.e())
# print(mock.e())

from unittest.mock import create_autospec

x = Exception('Bad', 'Wolf')
y = create_autospec(x)
print(isinstance(y, Exception))
print(y)

print('\n\nMagicMock..............')
from  unittest.mock import MagicMock

mock = MagicMock()
print(7 in mock)
print(mock.mock_calls)

mock.__contains__.return_value = True

print(8 in mock)
print(mock.mock_calls)

print(mock + 5)
print(mock.mock_calls)

mock += 5
print(mock.mock_calls)

mock = MagicMock()
x = mock
x += 5
print(x)
print(mock.mock_calls)
x += 10
print(x)
print(mock.mock_calls)

# Accessing a particular attribute is supposed to raise an AttributeError
# del mock.w
# mock.w


print('\n\nPropertyMock............')
from unittest.mock import PropertyMock

mock = Mock()
prop = PropertyMock()
type(mock).p = prop
print(mock.p)
print(mock.mock_calls)
print(prop.mock_calls)
mock.p = 6
print(prop.mock_calls)


print(type(Mock()) is type(Mock()))


print('\n\n Mocking file objects')
from unittest.mock import mock_open
open1 = mock_open(read_data='moose')
with open1('/fake/file/path.txt','r') as f:
    print(f.read())


print('\n\n Replacing real code with mock objects')
from unittest.mock import patch,mock_open
with patch('builtins.open', mock_open(read_data='moose')) as mock:
    with open('/fake/file.txt','r') as f:
        print(f.read())

print(open)
