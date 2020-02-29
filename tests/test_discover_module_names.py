from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_module_names


class TestDiscoverModuleNames(TestCase):

    def test_discover_module_names(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')
        expected_module0 = 'test_resources.module1'
        expected_module1 = 'test_resources.level2.module1'
        expected_module2 = 'test_resources.level2.module2'

        # EXECUTE
        modules = discover_module_names(path_to_resources)

        # VERIFY
        self.assertEqual(3, len(modules))
        self.assertIn(expected_module0, modules)
        self.assertIn(expected_module1, modules)
        self.assertIn(expected_module2, modules)
