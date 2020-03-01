from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_attributes, _match_attribute
from test_resources import module1


class TestDiscoverClasses(TestCase):

    def test_match_attribute(self):
        # EXECUTE
        match1 = _match_attribute('  some_attr   =     2  ')
        match2 = _match_attribute('  some_attr  :  int  =   2  ')
        match3 = _match_attribute(
            '  some_attr  :  int  =   2  #   bla bla bla!   ')

        # VERIFY
        self.assertTupleEqual(('some_attr', None, '2', None), match1)
        self.assertTupleEqual(('some_attr', 'int', '2', None), match2)
        self.assertTupleEqual(('some_attr', 'int', '2', 'bla bla bla!'), match3)

        # TODO add non-matches

    def test_discover_attributes_in_path(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        attributes = discover_attributes(path_to_resources)
        attribute_names = [attribute.name for attribute in attributes]

        # VERIFY
        self.assertEqual(2, len(attributes))
        self.assertListEqual(['ATTR1', 'ATTR1'], attribute_names)

    def test_discover_attributes_in_module(self):
        # EXECUTE
        attributes = discover_attributes(module1)

        # VERIFY
        self.assertEqual(1, len(attributes))
        self.assertEqual('ATTR1', attributes[0].name)
        self.assertEqual(int, attributes[0].type_)
        self.assertEqual(42, attributes[0].value)
        self.assertEqual('And some more comments here...', attributes[0].comment)

    def test_discover_attributes_in_private_modules(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        attributes = discover_attributes(path_to_resources, in_private_modules=True)

        # VERIFY
        self.assertEqual(3, len(attributes))
        self.assertTrue(all([attribute.is_public for attribute in attributes]))

    def test_discover_private_attributes(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        attributes = discover_attributes(path_to_resources, include_privates=True)

        # VERIFY
        self.assertEqual(4, len(attributes))
        self.assertTrue(any([attribute.is_private for attribute in attributes]))

    def test_discover_attributes_with_signature(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE
        attributes_str = discover_attributes(path_to_resources, signature=str)
        attributes_int = discover_attributes(path_to_resources, signature=int)

        # VERIFY
        self.assertEqual(1, len(attributes_str))
        self.assertEqual(1, len(attributes_int))
        self.assertEqual(str, attributes_str[0].type_)
        self.assertEqual(int, attributes_int[0].type_)

    def test_discover_attributes_with_wrong_argument(self):
        # EXECUTE & VALIDATE
        with self.assertRaises(ValueError):
            discover_attributes(123)
