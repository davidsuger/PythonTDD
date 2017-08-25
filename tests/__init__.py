from os import unlink


def setup():
    with open('test.tmp', 'w') as f:
        f.write('This is a test file.')


def teardown():
    unlink('test.tmp')
