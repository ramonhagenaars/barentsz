import sys
from pathlib import Path
from unittest import TestCase

from barentsz import discover_classes

sys.path.append(str(Path(__file__).parent.parent / 'test_resources'))

from examples_for_tests._private_module import PublicClass
from examples_for_tests.level2 import module1
from examples_for_tests.module1 import Class1, _PrivateClass
from examples_for_tests.level2.module1 import Class1 as Class1_level2


class TestDiscoverClasses(TestCase):

    def test_discover_classes_in_path(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

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
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        classes = discover_classes(path_to_resources, in_private_modules=True)

        # VERIFY
        self.assertEqual(3, len(classes))
        self.assertIn(Class1, classes)
        self.assertIn(Class1_level2, classes)
        self.assertIn(PublicClass, classes)

    def test_discover_private_classes(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        classes = discover_classes(path_to_resources, include_privates=True)

        # VERIFY
        self.assertEqual(3, len(classes))
        self.assertIn(Class1, classes)
        self.assertIn(Class1_level2, classes)
        self.assertIn(_PrivateClass, classes)

    def test_discover_classes_with_signature(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        classes = discover_classes(path_to_resources, include_privates=True, in_private_modules=True, signature=str)

        # VERIFY
        self.assertEqual(1, len(classes))
        self.assertIn(Class1, classes)

    def test_discover_classes_with_wrong_argument(self):
        # EXECUTE & VALIDATE
        with self.assertRaises(ValueError):
            discover_classes(123)

    def test_discover_classes_with_type_exclusions(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        # EXECUTE
        classes1 = discover_classes(path_to_resources, exclude=Class1)
        classes2 = discover_classes(path_to_resources, exclude=[Class1])

        # VERIFY
        self.assertEqual(1, len(classes1))
        self.assertIn(Class1_level2, classes1)
        self.assertEqual(1, len(classes2))
        self.assertIn(Class1_level2, classes2)

    def test_discover_classes_with_predicate_exclusions(self):
        # SETUP
        path_to_resources = (Path(__file__).parent.parent / 'test_resources'
                             / 'examples_for_tests')

        def _name_is_class1(cls: type) -> bool:
            return cls.__name__.lower() == 'class1'

        # EXECUTE
        classes1 = discover_classes(path_to_resources, exclude=_name_is_class1)
        classes2 = discover_classes(path_to_resources, exclude=[_name_is_class1])

        # VERIFY
        self.assertEqual(0, len(classes1))
        self.assertEqual(0, len(classes2))
