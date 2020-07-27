from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_packages


class TestDiscoverPackages(TestCase):

    def test_discover_packages(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')
        expected_package0 = 'examples_for_tests'
        expected_package1 = 'examples_for_tests.level2'

        # EXECUTE
        packages = discover_packages(path_to_resources)

        # VERIFY
        self.assertEqual(2, len(packages))
        self.assertIn(expected_package0, packages)
        self.assertIn(expected_package1, packages)

    def test_discover_packages_with_dir_thats_no_package(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests' / 'not_a_package')

        # EXECUTE & VERIFY
        with self.assertRaises(ValueError):
            discover_packages(path_to_resources)

    def test_discover_packages_with_dir_thats_doesnt_exist(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests' / 'does_not_exist')
        # EXECUTE & VERIFY
        with self.assertRaises(ValueError):
            discover_packages(path_to_resources)
