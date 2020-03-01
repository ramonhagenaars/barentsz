from unittest import TestCase

from barentsz._attribute import Attribute


class TestAttribute(TestCase):

    def test_is_private_or_public(self):
        # SETUP
        attribute1 = Attribute(
            name='attr',
            type_=int,
            value=42,
            doc='some doc',
            comment='some comment',
            hint='int',
            module=None,
            assigned_value='42',
            line='attr: int = 42',
            line_nr=-1)

        attribute2 = Attribute(
            name='_attr',
            type_=int,
            value=42,
            doc='some doc',
            comment='some comment',
            hint='int',
            module=None,
            assigned_value='42',
            line='attr: int = 42',
            line_nr=-1)

        # EXECUTE & VERIFY
        self.assertTrue(not attribute1.is_private)
        self.assertTrue(attribute1.is_public)
        self.assertTrue(attribute2.is_private)
        self.assertTrue(not attribute2.is_public)

    def test_is_constant(self):
        # SETUP
        attribute1 = Attribute(
            name='ATTR',
            type_=int,
            value=42,
            doc='some doc',
            comment='some comment',
            hint='int',
            module=None,
            assigned_value='42',
            line='attr: int = 42',
            line_nr=-1)

        # EXECUTE & VERIFY
        self.assertTrue(attribute1.is_constant)

    def test_eq(self):
        # SETUP
        attribute1 = Attribute(
            name='attr',
            type_=int,
            value=42,
            doc='some doc',
            comment='some comment',
            hint='int',
            module=None,
            assigned_value='42',
            line='attr: int = 42',
            line_nr=-1)

        attribute2 = Attribute(
            name='attr',
            type_=int,
            value=42,
            doc='some doc',
            comment='some comment',
            hint='int',
            module=None,
            assigned_value='42',
            line='attr: int = 42',
            line_nr=-1)

        # EXECUTE & VERIFY
        self.assertTrue(attribute1 is not attribute2)
        self.assertTrue(attribute1 == attribute2)
