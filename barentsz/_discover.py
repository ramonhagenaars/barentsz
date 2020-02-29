import glob
import inspect
import re
import sys
from importlib import import_module
from pathlib import Path
from typing import (
    Union,
    Dict,
    List,
    Any,
    Callable,
    Type,
    Iterable,
    Optional,
    Tuple,
)

from typish import Module, subclass_of, instance_of

from barentsz._attribute import Attribute


def discover_paths(directory: Union[Path, str], pattern: str) -> List[Path]:
    """
    Return a list of Paths within the given directory that match the given
    pattern.

    Args:
        directory: the directory in which is searched for paths.
        pattern: a pattern (example: '**/*.py').

    Returns: a list of Path objects.

    """
    directory_path = _path(directory)
    abspath = str(directory_path.absolute())
    sys.path.insert(0, abspath)
    path_to_discover = directory_path.joinpath(pattern)
    return [Path(filename) for filename in
            glob.iglob(str(path_to_discover), recursive=True)]


def discover_packages(directory: Union[Path, str]) -> List[str]:
    """
    Return a list of packages within the given directory. The directory must be
    a package.
    Args:
        directory: the directory in which is searched for packages.

    Returns: a list of packages.

    """
    return list(_discover_packages_per_path(directory).values())


def discover_module_names(
        directory: Union[Path, str],
        include_privates=False) -> List[str]:
    """
    Return a list of module names within the given directory. The directory
    must be a package and only names are returned of modules that are in
    packages.
    Args:
        directory: the directory in which is searched for modules.
        include_privates: if True, privates (unders and dunders) are also
        included.

    Returns: a list of module names (strings).

    """
    result = []
    packages_per_path = _discover_packages_per_path(directory)
    for path, package_name in packages_per_path.items():
        result.extend(['{}.{}'.format(package_name, p.stem)
                       for p in discover_paths(path, '*.py')
                       if p.stem != '__init__'
                       and (include_privates or not p.stem.startswith('_'))])
    return result


def discover_modules(
        directory: Union[Path, str],
        include_privates: bool = False,
        raise_on_fail: bool = False) -> List[Module]:
    """
    Return a list of modules within the given directory. The directory must be
    a package and only modules are returned that are in packages.
    Args:
        directory: the directory in which is searched for modules.
        include_privates: if True, privates (unders and dunders) are also
        included.
        raise_on_fail: if True, an ImportError is raised upon failing to
        import any module.

    Returns: a list of module objects.

    """
    modules = discover_module_names(directory, include_privates)
    result = []
    for module in modules:
        try:
            imported_module = import_module(module)
            result.append(imported_module)
        except Exception as err:
            if raise_on_fail:
                raise ImportError(err)
    return result


def discover_classes(
        source: Union[Path, str, Module, Iterable[Module]],
        signature: type = Any,
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[type]:
    elements = _discover_elements(source, inspect.isclass, include_privates,
                                  in_private_modules, raise_on_fail)
    return [cls for cls in elements
            if (signature is Any or subclass_of(cls, signature))]


def discover_functions(
        source: Union[Path, str, Module, Iterable[Module]],
        signature: Type[Callable] = Callable,
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[type]:
    elements = _discover_elements(source, inspect.isfunction, include_privates,
                                  in_private_modules, raise_on_fail)
    return [cls for cls in elements
            if (signature is Callable or instance_of(cls, signature))]


def discover_attributes(
        source: Union[Path, str, Module, Iterable[Module]],
        signature: type = Any,
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> Iterable[Attribute]:
    modules = _get_modules_from_source(source, in_private_modules, raise_on_fail)
    attributes = []
    for module in modules:
        with open(module.__file__) as module_file:
            lines = [line for line in module_file]
        for index, line in enumerate(lines):
            match = _match_attribute(line)
            if match:
                attribute = _create_attribute(*match, module, line, index + 1)
                if (instance_of(attribute.value, signature)
                        and (attribute.is_public or include_privates)):
                    attributes.append(attribute)
    return attributes


def _discover_elements(
        source: Union[Path, str, Module, Iterable[Module]],
        filter_: Callable[[Any], bool],
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[Any]:
    modules = _get_modules_from_source(source, in_private_modules, raise_on_fail)
    elements = [elem for module in modules
                for _, elem in inspect.getmembers(module, filter_)
                if (in_private_modules or not module.__name__.startswith('_'))
                and (include_privates or not elem.__name__.startswith('_'))]
    return elements


def _discover_packages_per_path(
        directory: Union[Path, str]) -> Dict[Path, str]:
    """
    Discover packages and their original Paths within the given directory.
    Args:
        directory: the directory in which is searched for modules.

    Returns: a dict with Paths as keys and strings (the package names) as
    values.

    """
    directory_path = _path(directory)
    if not directory_path.exists():
        raise ValueError('The given directory does not exist. '
                         'Given: {}'.format(directory))
    if not _is_package(directory_path):
        raise ValueError('The given directory must itself be a package. '
                         'Given: {}'.format(directory))

    paths_to_inits = discover_paths(directory_path, '**/__init__.py')
    paths = [p.parent for p in paths_to_inits]
    packages_per_path = {p: _to_package_name(p) for p in paths}

    # All packages must have a straight line of packages from the base package.
    base_package = _to_package_name(directory_path)
    result = {path: package for path, package in packages_per_path.items()
              if package.startswith(base_package)}

    return result


def _path(directory: Union[Path, str]) -> Path:
    """
    Return a path if directory is a string or return directory if it is a Path
    already. Raise a ValueError if it is neither a Path nor a string.

    Args:
        directory: the directory that is a string or Path.

    Returns: a Path instance.

    """
    if isinstance(directory, Path):
        result = directory
    elif isinstance(directory, str):
        result = Path(directory)
    else:
        raise ValueError('Invalid type ({}) for directory, provide a Path or '
                         'a string.'.format(type(directory)))
    return result


def _get_modules_from_source(
        source: Union[Path, str, Module, Iterable[Module]],
        in_private_modules: bool = False,
        raise_on_fail: bool = False
) -> Iterable[Module]:
    """
    Get an iterable of Modules from the given source.
    Args:
        source: anything that can be turned into an iterable of Modules.
        in_private_modules: if True, private modules are returned as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.

    Returns: an iterable of Module instances.

    """
    if isinstance(source, Path):
        modules = discover_modules(source, in_private_modules, raise_on_fail)
    elif isinstance(source, str):
        modules = discover_modules(Path(source), in_private_modules,
                                   raise_on_fail)
    elif isinstance(source, Module):
        modules = [source]
    elif instance_of(source, Iterable[Module]):
        modules = source
    else:
        raise ValueError('The given source must be a Path, string or module. '
                         'Given: {}'.format(source))
    return modules


def _match_attribute(line: str) -> Optional[Tuple[str, str, str, str]]:
    """
    Try to match the given line with an attribute and return the name,
    type hint, value and inline comment (respectively) if a match was
    found.

    Args:
        line: the line of code that (may) contain an attribute declaration.

    Returns: a tuple with strings (name, hint, value, comment) or None.

    """
    attr_pattern = re.compile(
        '^'
        '\s*'
        '([a-zA-Z_]+[a-zA-Z_0-9]*)'  # 1: Name.
        '(\s*:\s*(\w+)\s*)?'  # 3: Type hint.
        '\s*=\s*'
        '(.+?)'  # 4: Value.
        '\s*'
        '(#\s*(.*?)\s*)?'  # 6: Inline comment.
        '$'
    )
    match = attr_pattern.match(line)
    if match:
        attr_name = match.group(1)
        hint = match.group(3)
        attr_value = match.group(4)
        inline_comments = match.group(6)
        return attr_name, hint, attr_value, inline_comments


def _create_attribute(
        name: str,
        hint: Optional[str],
        assigned_value: str,
        comment: Optional[str],
        module: Module,
        line: str,
        line_nr: int) -> Attribute:
    """
    Create and return an Attribute instance from the given parameters.
    Args:
        name: the name of the attribute.
        hint: the type hint of the attribute (if any).
        assigned_value: the string that was literally assigned.
        comment: an inline comment (if any).
        module: the module that contains the attribute.
        line: the line that defines the attribute.
        line_nr: the line number of the attribute.

    Returns: an Attribute instance.

    """
    value = getattr(module, name)
    type_ = type(value)
    return Attribute(
        name=name,
        type_=type_,
        value=value,
        doc=None,
        comment=comment,
        hint=hint,
        module=module,
        assigned_value=assigned_value,
        line=line,
        line_nr=line_nr
    )


def _is_package(directory: Path) -> bool:
    paths = discover_paths(directory, '__init__.py')
    return len(paths) > 0


def _to_package_name(directory: Path) -> str:
    parts = []
    current_dir = directory
    while _is_package(current_dir):
        # See how far up the tree we can go while still in a package.
        parts.insert(0, current_dir.stem)
        current_dir = current_dir.parent
    return '.'.join(parts)