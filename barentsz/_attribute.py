from typing import Any, Optional

from typish import Module


class Attribute:
    def __init__(
            self,
            name: str,
            type_: type,
            value: Any,
            doc: Optional[str],
            comment: Optional[str],
            hint: str,
            module: Module,
            assigned_value: str,
            line: str,
            line_nr: int):
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
        return self.name.startswith('_')

    @property
    def is_public(self) -> bool:
        return not self.is_private

    @property
    def is_constant(self) -> bool:
        return self.name.isupper()

    def __eq__(self, other: 'Attribute') -> bool:
        return (isinstance(other, Attribute)
                and other.name == self.name
                and other.value == self.value
                and other.type_ == self.type_
                and other.module == self.module
                and other.line_nr == self.line_nr)
