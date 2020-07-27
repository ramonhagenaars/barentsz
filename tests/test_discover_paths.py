from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_paths


class TestDiscoverPaths(TestCase):

    def test_discover_paths(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')
        expected0 = path_to_resources / 'module1.py'
        expected1 = path_to_resources / '__init__.py'
        expected2 = path_to_resources / '_private_module.py'
        expected3 = path_to_resources / 'level2/module1.py'
        expected4 = path_to_resources / 'level2/module2.py'
        expected5 = path_to_resources / 'level2/__init__.py'
        expected6 = path_to_resources / 'not_a_package/module3.py'
        expected7 = path_to_resources / 'not_a_package/is_a_package/module5.py'
        expected8 = path_to_resources / 'not_a_package/is_a_package/__init__.py'

        # EXECUTE
        paths = discover_paths(path_to_resources, '**/*.py')

        # VERIFY
        self.assertEqual(9, len(paths))
        self.assertIn(expected0, paths)
        self.assertIn(expected1, paths)
        self.assertIn(expected2, paths)
        self.assertIn(expected3, paths)
        self.assertIn(expected4, paths)
        self.assertIn(expected5, paths)
        self.assertIn(expected6, paths)
        self.assertIn(expected7, paths)
        self.assertIn(expected8, paths)

    def test_discover_paths_with_a_string(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')
        expected0 = path_to_resources / 'module1.py'
        expected1 = path_to_resources / '__init__.py'
        expected2 = path_to_resources / '_private_module.py'
        expected3 = path_to_resources / 'level2/module1.py'
        expected4 = path_to_resources / 'level2/module2.py'
        expected5 = path_to_resources / 'level2/__init__.py'
        expected6 = path_to_resources / 'not_a_package/module3.py'
        expected7 = path_to_resources / 'not_a_package/is_a_package/module5.py'
        expected8 = path_to_resources / 'not_a_package/is_a_package/__init__.py'

        # EXECUTE
        paths = discover_paths(str(path_to_resources), '**/*.py')

        # VERIFY
        self.assertEqual(9, len(paths))
        self.assertIn(expected0, paths)
        self.assertIn(expected1, paths)
        self.assertIn(expected2, paths)
        self.assertIn(expected3, paths)
        self.assertIn(expected4, paths)
        self.assertIn(expected5, paths)
        self.assertIn(expected6, paths)
        self.assertIn(expected7, paths)
        self.assertIn(expected8, paths)

    def test_discover_paths_with_wrong_arg_type(self):
        # EXECUTE & VERIFY
        with self.assertRaises(ValueError):
            discover_paths({}, '**/*.py')
