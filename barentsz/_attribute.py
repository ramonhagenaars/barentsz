from typing import Any, Optional

from typish import Module


class Attribute:
    """
    Represents an attribute of a module.
    """

    def __init__(
            self,
            name: str,
            type_: type,
            value: Any,
            doc: Optional[str],
            comment: Optional[str],
            hint: Optional[str],
            module: Module,
            assigned_value: str,
            line: str,
            line_nr: int):
        """
        Constructor.
        :param name: the name of the attribute.
        :param type_: the actual type of the attribute.
        :param value: the actual value of the attribute.
        :param doc: any docstring on top of the attribute.
        :param comment: any inline comment behind the attribute.
        :param hint: the hinted type of the attribute.
        :param module: the module that contains the attribute.
        :param assigned_value: the value that was assigned.
        :param line: the line that defines the attribute.
        :param line_nr: the line number that holds the attribute.
        """
        self.name = name
        self.type_ = type_
        self.value = value
        self.doc = doc
        self.comment = comment
        self.hint = hint
        self.module = module
        self.assigned_value = assigned_value
        self.line = line
        self.line_nr = line_nr

    @property
    def is_private(self) -> bool:
        """
        Return whether this attribute is marked as private.
        :return: True if this attribute is supposed to be private.
        """
        return self.name.startswith('_')

    @property
    def is_public(self) -> bool:
        """
        Return whether this attribute is public.
        :return: True if this attribute is not private.
        """
        return not self.is_private

    @property
    def is_constant(self) -> bool:
        """
        Return whether this attribute is supposed to be a constant.
        :return: True when this attribute is supposed to be a constant.
        """
        return self.name.isupper()

    def __eq__(self, other: object) -> bool:
        """
        Compare this attribute with other and check if they are equal.
        :param other: another attribute instance.
        :return: True if both instances are considered to be equal.
        """
        return (isinstance(other, Attribute)
                and other.name == self.name
                and other.value == self.value
                and other.type_ == self.type_
                and other.module == self.module
                and other.line_nr == self.line_nr)
