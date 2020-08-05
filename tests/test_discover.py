import sys
from pathlib import Path
from typing import List
from unittest import TestCase

sys.path.append(str(Path(__file__).parent.parent / 'test_resources'))

from examples_for_tests.level2.module1 import Class1 as Class1Level2
from examples_for_tests.module1 import Class1

from barentsz import discover, here

sys.path.append(str(Path(__file__).parent.parent / 'test_resources'))


class TestDiscoverClasses(TestCase):

    def test_discover(self):
        # EXECUTE
        discoveries = discover()

        # VERIFY
        self.assertIn('TestDiscoverClasses', [cls.__name__ for cls in discoveries])

    def test_discover_list_of_classes(self):
        # SETUP
        path_to_resources = (here().parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        # discoveries = discover(path_to_resources, what=List[type])

        discoveries: List[type] = discover(path_to_resources)

        # VERIFY
        self.assertEqual(2, len(discoveries))
        self.assertIn(Class1, discoveries)
        self.assertIn(Class1Level2, discoveries)

    def test_discover_list(self):
        # SETUP
        path_to_resources = (here().parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        discoveries1 = discover(path_to_resources, what=list)
        discoveries2 = discover(path_to_resources, what=List)

        # VERIFY
        self.assertEqual(2, len(discoveries1))
        self.assertIn(Class1, discoveries1)
        self.assertIn(Class1Level2, discoveries1)

        self.assertEqual(2, len(discoveries2))
        self.assertIn(Class1, discoveries2)
        self.assertIn(Class1Level2, discoveries2)

    def test_discover_not_supported(self):
        # SETUP
        path_to_resources = (here().parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        with self.assertRaises(ValueError) as err:
            discover(path_to_resources, what=int)

        # VERIFY
        self.assertIn('int', str(err.exception))
