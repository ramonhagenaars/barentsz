from pathlib import Path
from typing import Callable
from unittest import TestCase

from barentsz._discover import discover_functions

import sys

sys.path.append(str(Path(__file__).parent.parent / 'test_resources'))
from examples_for_tests._private_module import (
    _private_function as private_module_private_function,
    public_function,
)
from examples_for_tests.level2 import module1 as module1_level2
from examples_for_tests.level2.module1 import function1 as function1_level2
from examples_for_tests.module1 import function1, _private_function


class TestDiscoverFunctions(TestCase):

    def test_discover_functions_in_path(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        functions = discover_functions(path_to_resources)

        # VERIFY
        self.assertEqual(2, len(functions))
        self.assertIn(function1, functions)
        self.assertIn(function1_level2, functions)

    def test_discover_functions_in_module(self):
        # EXECUTE
        functions = discover_functions(module1_level2)

        # VERIFY
        self.assertEqual(1, len(functions))
        self.assertIn(function1_level2, functions)

    def test_discover_functions_in_class(self):
        # SETUP
        class C:
            def f1(self):
                ...

            def _f2(self):
                ...

            @staticmethod
            def f3():
                ...

            @classmethod
            def f4(cls):
                ...

        # EXECUTE
        functions = discover_functions(C, include_privates=True)

        # VERIFY
        self.assertEqual(4, len(functions))
        self.assertIn(C.f1, functions)
        self.assertIn(C._f2, functions)
        self.assertIn(C.f3, functions)
        self.assertIn(C.f4, functions)

    def test_discover_functions_in_private_modules(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        functions = discover_functions(path_to_resources, in_private_modules=True)

        # VERIFY
        self.assertEqual(3, len(functions))
        self.assertIn(function1, functions)
        self.assertIn(function1_level2, functions)
        self.assertIn(public_function, functions)

    def test_discover_private_functions(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        functions = discover_functions(path_to_resources, include_privates=True)

        # VERIFY
        self.assertEqual(3, len(functions))
        self.assertIn(function1, functions)
        self.assertIn(function1_level2, functions)
        self.assertIn(_private_function, functions)

    def test_discover_functions_with_signature(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        functions = discover_functions(path_to_resources,
                                       include_privates=True,
                                       in_private_modules=True,
                                       signature=Callable[[int, float], str])

        # VERIFY
        self.assertEqual(1, len(functions))
        self.assertIn(private_module_private_function, functions)

    def test_discover_functions_with_wrong_argument(self):
        # EXECUTE & VALIDATE
        with self.assertRaises(ValueError):
            discover_functions(123)
