

"""

Lets put some
comments for ATTR1 here

with multiple lines...
"""
ATTR1   : int   = 42    #   And some more comments here...
_PRIVATE_ATTR = 42


class Class1(str):
    def method(self):
        raise NotImplementedError


class _PrivateClass:
    def _privateMethod(self):
        raise NotImplementedError


def _private_function():
    raise NotImplementedError


def function1():
    raise NotImplementedError
