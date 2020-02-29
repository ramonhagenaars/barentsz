from pathlib import Path
from typing import Callable
from unittest import TestCase

from barentsz._discover import discover_functions
from test_resources._private_module import (
    _private_function as private_module_private_function,
    public_function
)
from test_resources.level2 import module1 as module1_level2
from test_resources.level2.module1 import function1 as function1_level2
from test_resources.module1 import function1, _private_function


class TestDiscoverFunctions(TestCase):

    def test_discover_functions_in_path(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

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

    def test_discover_functions_in_private_modules(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        functions = discover_functions(path_to_resources, in_private_modules=True)

        # VERIFY
        self.assertEqual(3, len(functions))
        self.assertIn(function1, functions)
        self.assertIn(function1_level2, functions)
        self.assertIn(public_function, functions)

    def test_discover_private_functions(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        functions = discover_functions(path_to_resources, include_privates=True)

        # VERIFY
        self.assertEqual(3, len(functions))
        self.assertIn(function1, functions)
        self.assertIn(function1_level2, functions)
        self.assertIn(_private_function, functions)

    def test_discover_functions_with_signature(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

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
