import sys
import os

# Allow tests to be run from self
sys.path.insert(0, os.path.abspath('./src/'))

# Add capture context_manager to test sys.out
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from contextlib import contextmanager

@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out
