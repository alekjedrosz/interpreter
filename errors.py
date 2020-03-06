import sys


def error(lineno, msg):
    err = f'\nLine {lineno}: {msg}\n'
    sys.stderr.write(err)
    exit()
