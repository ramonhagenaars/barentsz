from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_modules, _get_modules_from_source


class TestDiscoverModules(TestCase):

    def test_discover_modules(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')
        expected_module0 = 'examples_for_tests.module1'
        expected_module1 = 'examples_for_tests.level2.module1'

        # EXECUTE
        modules = discover_modules(path_to_resources)
        module_names = [module.__name__ for module in modules]

        # VERIFY
        self.assertEqual(2, len(modules))
        self.assertIn(expected_module0, module_names)
        self.assertIn(expected_module1, module_names)

    def test_discover_modules_with_raise(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE & VERIFY
        with self.assertRaises(ImportError):
            # test_resources.level2.module2 has invalid syntax.
            discover_modules(path_to_resources, raise_on_fail=True)

    def test_get_modules_from_source(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests' / 'level2')
        str_path_to_resources = str(path_to_resources)

        # EXECUTE
        a = _get_modules_from_source(path_to_resources)
        b = _get_modules_from_source(str_path_to_resources)
        c = _get_modules_from_source(a)
        d = _get_modules_from_source(b[0])

        # VERIFY
        self.assertTrue(a == b == c == d)
