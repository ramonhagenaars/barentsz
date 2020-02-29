from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_classes
from test_resources._private_module import PublicClass
from test_resources.level2 import module1
from test_resources.level2.module1 import Class1 as Class1_level2
from test_resources.module1 import Class1, _PrivateClass


class TestDiscoverClasses(TestCase):

    def test_discover_classes_in_path(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        classes = discover_classes(path_to_resources)

        # VERIFY
        self.assertEqual(2, len(classes))
        self.assertIn(Class1, classes)
        self.assertIn(Class1_level2, classes)

    def test_discover_classes_in_module(self):
        # EXECUTE
        classes = discover_classes(module1)

        # VERIFY
        self.assertEqual(1, len(classes))
        self.assertIn(Class1_level2, classes)

    def test_discover_classes_in_private_modules(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        classes = discover_classes(path_to_resources, in_private_modules=True)

        # VERIFY
        self.assertEqual(3, len(classes))
        self.assertIn(Class1, classes)
        self.assertIn(Class1_level2, classes)
        self.assertIn(PublicClass, classes)

    def test_discover_private_classes(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        classes = discover_classes(path_to_resources, include_privates=True)

        # VERIFY
        self.assertEqual(3, len(classes))
        self.assertIn(Class1, classes)
        self.assertIn(Class1_level2, classes)
        self.assertIn(_PrivateClass, classes)

    def test_discover_classes_with_signature(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        classes = discover_classes(path_to_resources, include_privates=True, in_private_modules=True, signature=str)

        # VERIFY
        self.assertEqual(1, len(classes))
        self.assertIn(Class1, classes)

    def test_discover_classes_with_wrong_argument(self):
        # EXECUTE & VALIDATE
        with self.assertRaises(ValueError):
            discover_classes(123)