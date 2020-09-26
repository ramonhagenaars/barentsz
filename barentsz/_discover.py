import glob
import re
import sys
from importlib import import_module
from inspect import (
    getmembers,
    isclass,
    isfunction,
    ismethod,
)
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typish import (
    Module,
    instance_of,
    subclass_of,
)

from barentsz._attribute import Attribute
from barentsz._here import here
from barentsz._typings import ClsPredicate


def discover(
        source: Any = None,
        *,
        what: Any = List[type],
        **kwargs: dict,
) -> list:
    """
    Convenience function for discovering types in some source. If not source
    is given, the directory is used in which the calling module is located.

    Args:
        source: the source in which is searched or the directory of the
        caller if None.
        what: the type that is to be discovered.
        **kwargs: any keyword argument that is passed on.

    Returns: a list of discoveries.

    """
    source = source or here(1)

    delegates = [
        (List[type], _discover_list),
        (list, _discover_list),
        (List, _discover_list),
    ]

    for tuple_ in delegates:
        type_, delegate = tuple_
        if subclass_of(what, type_):
            return delegate(what, source, **kwargs)

    accepted_types = ', '.join(['`{}`'.format(delegate)
                                for delegate, _ in delegates])
    raise ValueError('Type `{}` is not supported. This function accepts: '
                     '{}'.format(what, accepted_types))


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
    result = [Path(filename) for filename in
              glob.iglob(str(path_to_discover), recursive=True)]
    result.sort()
    return result


def discover_packages(directory: Union[Path, str]) -> List[str]:
    """
    Return a list of packages within the given directory. The directory must be
    a package.
    Args:
        directory: the directory in which is searched for packages.

    Returns: a list of packages.

    """
    result = list(_discover_packages_per_path(directory).values())
    result.sort()
    return result


def discover_module_names(
        directory: Union[Path, str],
        include_privates: bool = False) -> List[str]:
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
    result.sort()
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
                raise ImportError(err) from err
    result.sort(key=lambda module: module.__name__)
    return result


def discover_classes(
        source: Union[Path, str, Module, Iterable[Module]],
        signature: type = Any,  # type: ignore
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False,
        exclude: Union[type, ClsPredicate,
                       Iterable[Union[type, ClsPredicate]]] = None
) -> List[type]:
    """
    Discover any classes within the given source and according to the given
    constraints.

    Args:
        source: the source in which is searched for any classes.
        signature: only classes that inherit from signature are returned.
        include_privates: if True, private classes are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.
        exclude: one or more types or predicates that are to be excluded
        from the result.

    Returns: a list of all discovered classes (types).

    """
    exclude_ = _ensure_set(exclude)
    elements = _discover_elements(source, isclass, include_privates,
                                  in_private_modules, raise_on_fail)
    result = list({cls for cls in elements
                   if (signature is Any or subclass_of(cls, signature))
                   and cls not in exclude_})

    exclude_predicates = (e for e in exclude_ if isfunction(e))
    for pred in exclude_predicates:
        result = [cls for cls in result if not pred(cls)]  # type: ignore[operator] # noqa
    result.sort(key=lambda cls: cls.__name__)
    return result


def discover_functions(
        source: Union[Path, str, Module, Iterable[Module], type],
        signature: Type[Callable] = Callable,  # type: ignore
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[type]:
    """
    Discover any functions within the given source and according to the given
    constraints.

    Args:
        source: the source in which is searched for any functions.
        signature: only functions that have this signature (parameters and
        return type) are included.
        include_privates: if True, private functions are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.

    Returns: a list of all discovered functions.

    """

    def filter_(*args_: Iterable[Any]) -> bool:
        return (isfunction(*args_)
                or ismethod(*args_))

    if not isinstance(source, type):
        filter_ = isfunction  # type: ignore

    elements = _discover_elements(source, filter_, include_privates,
                                  in_private_modules, raise_on_fail)
    result = [elem for elem in elements
              if (signature is Callable or instance_of(elem, signature))]
    result.sort(key=lambda func: func.__name__)
    return result


def discover_attributes(
        source: Union[Path, str, Module, Iterable[Module]],
        signature: type = Any,  # type: ignore
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[Attribute]:
    """
    Discover any attributes within the given source and according to the given
    constraints.

    Args:
        source: the source in which is searched for any attributes.
        signature: only attributes that are subtypes of this signature are
        included.
        include_privates: if True, private attributes are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.

    Returns: a list of all discovered attributes.

    """
    modules = _get_modules_from_source(source, in_private_modules,
                                       raise_on_fail)
    attributes: List[Attribute] = []
    for module in modules:
        with open(module.__file__) as module_file:
            lines = list(module_file)
        attributes += _discover_attributes_in_lines(
            lines, module, signature, include_privates)
    attributes.sort(key=lambda attr: attr.name)
    return attributes


def _discover_attributes_in_lines(
        lines: List[str],
        module: Module,
        signature: type,
        include_privates: bool) -> List[Attribute]:
    """
    Discover any attributes within the lines of codee and according to the
    given constraints.

    Args:
        lines: the lines of code in which is searched for any attributes.
        module: the module from which these lines originate.
        signature: only attributes that are subtypes of this signature are
        included.
        include_privates: if True, private attributes are included as well.

    Returns: a list of all discovered attributes.

    """
    attributes = []
    for index, line in enumerate(lines):
        match = _match_attribute(line)
        if match:
            name, hint, value, comment = match
            docstring = _find_attribute_docstring(lines[0:index])
            attribute = _create_attribute(name, hint, value, docstring,
                                          comment, module, line, index + 1)
            if (instance_of(attribute.value, signature)
                    and (attribute.is_public or include_privates)):
                attributes.append(attribute)
    return attributes


def _discover_elements(
        source: Union[Path, str, Module, Iterable[Module], type],
        filter_: Callable[[Any], bool],
        include_privates: bool = False,
        in_private_modules: bool = False,
        raise_on_fail: bool = False) -> List[Any]:
    """
    Discover elements (such as attributes or functions) in the given source.
    Args:
        source: the source that is explored.
        filter_: the filter that determines the type of element.
        include_privates: if True, private elements are returned as well.
        in_private_modules: if True, private modules are examined as well.
        raise_on_fail: if True, an ImportError will be raised upon import
        failure.

    Returns: a list of elements.

    """
    if isinstance(source, type):
        sources = [source]  # type: Iterable
    else:
        sources = _get_modules_from_source(source, in_private_modules,
                                           raise_on_fail)

    elements = [elem for src in sources
                for _, elem in getmembers(src, filter_)
                if (in_private_modules or not src.__name__.startswith('_'))
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
        in_private_modules: if True, private modules are explored as well.
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
        modules = source  # type: ignore
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
        r'^'
        r'\s*'
        r'([a-zA-Z_]+[a-zA-Z_0-9]*)'  # 1: Name.
        r'(\s*:\s*(\w+)\s*)?'  # 3: Type hint.
        r'\s*=\s*'
        r'(.+?)'  # 4: Value.
        r'\s*'
        r'(#\s*(.*?)\s*)?'  # 6: Inline comment.
        r'$'
    )
    match = attr_pattern.match(line)
    result = None
    if match:
        attr_name = match.group(1)
        hint = match.group(3)
        attr_value = match.group(4)
        inline_comments = match.group(6)
        result = attr_name, hint, attr_value, inline_comments
    return result


def _create_attribute(
        name: str,
        hint: Optional[str],
        assigned_value: str,
        docstring: Optional[str],
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
        docstring: the docstring above this attribute.
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
        doc=docstring,
        comment=comment,
        hint=hint,
        module=module,
        assigned_value=assigned_value,
        line=line,
        line_nr=line_nr
    )


def _is_package(directory: Path) -> bool:
    """
    Return True if the given directory is a package and False otherwise.
    Args:
        directory: the directory to check.

    Returns: True if directory is a package.

    """
    paths = discover_paths(directory, '__init__.py')
    return len(paths) > 0


def _to_package_name(directory: Path) -> str:
    """
    Translate the given directory to a package (str). Check every parent
    directory in the tree to find the complete fully qualified package name.
    Args:
        directory: the directory that is to become a package name.

    Returns: a package name as string.

    """
    parts: List[str] = []
    current_dir = directory.absolute()
    while _is_package(current_dir):
        # See how far up the tree we can go while still in a package.
        parts.insert(0, current_dir.stem)
        current_dir = current_dir.parent
    return '.'.join(parts)


def _find_attribute_docstring(lines: List[str]) -> Optional[str]:
    """
    Find any docstring that is right above an attribute.
    Args:
        lines: the lines of code that may contain a docstring.

    Returns: a docstring (str) or None.

    """
    result = None
    if lines:
        joined_lines = ''.join(lines).strip()
        docstring_pattern = re.compile(
            r'("{3}\s*([\s\S]+)\s*"{3}|'  # 2: docstring content.
            r'\'{3}\s*([\s\S]+)\s*\'{3})'  # 3: docstring content.
            r'$'
        )
        match = docstring_pattern.match(joined_lines)
        if match:
            result = (match.group(2) or match.group(3)).strip()
    return result


def _ensure_set(arg: Union[object, Iterable[object]]) -> Set[object]:
    # Make sure that arg is a set.
    result = arg or set()
    if not isinstance(result, Iterable):
        result = {result}
    else:
        result = set(result)
    return result


def _discover_list(
        what_: List[type],
        source: Union[Path, str, Module, Iterable[Module]],
        **kwargs: dict) -> List[type]:
    args = getattr(what_, '__args__', None) or [Any]
    signature = args[0]
    if signature in (type, Type) or isinstance(signature, TypeVar):  # type: ignore[arg-type] # noqa
        signature = Any
    kwargs['signature'] = signature
    return discover_classes(source, **kwargs)  # type: ignore[arg-type]
