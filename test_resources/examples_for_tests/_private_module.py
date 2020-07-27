ATTR1 = 42
_PRIVATE_ATTR = 42


class PublicClass:
    def _privateMethod(self):
        raise NotImplementedError


class _PrivateClass:
    def _privateMethod(self):
        raise NotImplementedError


def public_function(x: float, y: int) -> int:
    raise NotImplementedError


def _private_function(x: int, y: float) -> str:
    raise NotImplementedError

