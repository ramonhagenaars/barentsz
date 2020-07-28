[![Python versions](https://img.shields.io/pypi/pyversions/barentsz.svg)](https://img.shields.io/pypi/pyversions/barentsz.svg)
[![PyPI version](https://badge.fury.io/py/barentsz.svg)](https://badge.fury.io/py/barentsz)
![barentsz](https://github.com/ramonhagenaars/barentsz/workflows/barentsz/badge.svg)

# Barentsz

⛵ Explore and discover modules, classes, functions, attributes.

<a href='https://en.wikipedia.org/wiki/Svalbard'>
<img width='100%' src='https://lh3.googleusercontent.com/7YPQsyFF_rE-j2yVnUiudk_CjWt4THrAK2JJFS7HUBPcRXd7UuD382C9EqYeQecvtzLJsEckQjuhcgbAs41FwIE9WOEM3AlPBSJx55qLgqok9Qn_FAsL0NtmMdUTX0yvxiO4RkN-NXXCOQGhpErST8HfWk7qd_25m-hPN9zJEwZNK_8RVdX80odzyCD7ucXv3TYKPeY3wLQxjW_mjvYD0Q6ieZtW-PhYBrjjfMOKGbTzZIJ42KyPE3t40LB-yQOBXn-48H0v_N4tGmoU1beGt6nC_kpu0sUIlttCq57ajW7FIPBpUWVm4HkmL3-ndFzu16gY1XxH6uJf4Pl1opfofRaMsY1OhUll9xjfrHsWL8MQjbA4ZmHjSnJvk790lO_HaicdC9VV3lcnUSJFUlGL7u3dS3SXznQPDebJeCavBBjxN12ur440b0Hp-JGw75Dw4SjC76tIabqy1big5ilZaNk9UgOTVUwXwC7-ZDV3Aufj6-8rcepOvP3ple1fWHfxeDPpkEkhL6WTobfqIqvT17UFubWz0CnhAmd-Mq6Y9tlp4rn3xL8rwKs91YDhh6ev0KslCm1bW8KMIKfUWselrchIsJcTRchQGr8ubN-0w0USvO92Z6txFVRsuKvl-sJUMGzooS_deu2J_wiFZK1KoVGh-QvI4dTAqgp-cxVh0jkqqyc90Pzt7bSmJJK2IfMkReCJ0YdZDxE6Abs0bGIX3qYd7VZy6AqXqQpzTKnyzcoT-T2c=w1920-h429-no' />
</a>

```
pip install barentsz
```

## ❄ Overview

* Discover all packages in a path;
* Discover all modules in a path;
* Discover all/some classes in a path or module;
* Discover all/some functions in a path, module or class;
* Discover all/some attributes in a path or module.

## ❄ Features in detail

### Discover Classes

##### Import
```python
>>> from barentsz import discover_classes

```

##### Usage Example
```python
>>> discover_classes('./test_resources/examples_for_readme')
[<class 'examples_for_readme.module_a.ClassA'>, <class 'examples_for_readme.module_b.ClassB'>]

```

##### Help documentation
```python
>>> help(discover_classes)
Help on function discover_classes in module barentsz._discover:
<BLANKLINE>
discover_classes(source: Union[pathlib.Path, str, module, Iterable[module]], signature: type = typing.Any, include_privates: bool = False, in_private_modules: bool = False, raise_on_fail: bool = False) -> List[type]
    Discover any classes within the given source and according to the given
    constraints.
<BLANKLINE>
    Args:
        source: the source in which is searched for any classes.
        signature: only classes that inherit from signature are returned.
        include_privates: if True, private classes are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.
<BLANKLINE>
    Returns: a list of all discovered classes (types).
<BLANKLINE>

```

### Discover Functions

##### Import
```python
>>> from barentsz import discover_functions

```

##### Usage Example
```python
>>> functions = discover_functions('./test_resources/examples_for_readme')
>>> [f.__name__ for f in functions]
['function_a', 'function_b']

```

##### Help documentation
```python
>>> help(discover_functions)
Help on function discover_functions in module barentsz._discover:
<BLANKLINE>
discover_functions(source: Union[pathlib.Path, str, module, Iterable[module], type], signature: Type[Callable] = typing.Callable, include_privates: bool = False, in_private_modules: bool = False, raise_on_fail: bool = False) -> List[type]
    Discover any functions within the given source and according to the given
    constraints.
<BLANKLINE>
    Args:
        source: the source in which is searched for any functions.
        signature: only functions that have this signature (parameters and
        return type) are included.
        include_privates: if True, private functions are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.
<BLANKLINE>
    Returns: a list of all discovered functions.
<BLANKLINE>

```

### Discover Attributes

##### Import
```python
>>> from barentsz import discover_attributes

```

##### Usage Example
```python
>>> attributes = discover_attributes('./test_resources/examples_for_readme')
>>> [a.name for a in attributes]
['attr_a', 'attr_b']

```

##### Help documentation
```python
>>> help(discover_attributes)
Help on function discover_attributes in module barentsz._discover:
<BLANKLINE>
discover_attributes(source: Union[pathlib.Path, str, module, Iterable[module]], signature: type = typing.Any, include_privates: bool = False, in_private_modules: bool = False, raise_on_fail: bool = False) -> List[barentsz._attribute.Attribute]
    Discover any attributes within the given source and according to the given
    constraints.
<BLANKLINE>
    Args:
        source: the source in which is searched for any attributes.
        signature: only attributes that are subtypes of this signature are
        included.
        include_privates: if True, private attributes are included as well.
        in_private_modules: if True, private modules are explored as well.
        raise_on_fail: if True, raises an ImportError upon the first import
        failure.
<BLANKLINE>
    Returns: a list of all discovered attributes.
<BLANKLINE>

```

### Discover Modules

##### Import
```python
>>> from barentsz import discover_modules

```

##### Usage Example
```python
>>> modules = discover_modules('./test_resources/examples_for_readme')
>>> [m.__name__ for m in modules]
['examples_for_readme.module_a', 'examples_for_readme.module_b']

```

##### Help documentation
```python
>>> help(discover_modules)
Help on function discover_modules in module barentsz._discover:
<BLANKLINE>
discover_modules(directory: Union[pathlib.Path, str], include_privates: bool = False, raise_on_fail: bool = False) -> List[module]
    Return a list of modules within the given directory. The directory must be
    a package and only modules are returned that are in packages.
    Args:
        directory: the directory in which is searched for modules.
        include_privates: if True, privates (unders and dunders) are also
        included.
        raise_on_fail: if True, an ImportError is raised upon failing to
        import any module.
<BLANKLINE>
    Returns: a list of module objects.
<BLANKLINE>


```

### Discover Packages

##### Import
```python
>>> from barentsz import discover_packages

```

##### Usage Example
```python
>>> discover_packages('./test_resources/examples_for_readme')
['examples_for_readme']

```

##### Help documentation
```python
>>> help(discover_packages)
Help on function discover_packages in module barentsz._discover:
<BLANKLINE>
discover_packages(directory: Union[pathlib.Path, str]) -> List[str]
    Return a list of packages within the given directory. The directory must be
    a package.
    Args:
        directory: the directory in which is searched for packages.
<BLANKLINE>
    Returns: a list of packages.
<BLANKLINE>

```

### Discover Paths

##### Import
```python
>>> from barentsz import discover_paths

```

##### Usage Example
```python
>>> paths = discover_paths('./test_resources/examples_for_readme', '**/*.py')
>>> [str(p.as_posix()) for p in paths]
['test_resources/examples_for_readme/module_a.py', 'test_resources/examples_for_readme/module_b.py', 'test_resources/examples_for_readme/__init__.py']

```

##### Help documentation
```python
>>> help(discover_paths)
Help on function discover_paths in module barentsz._discover:
<BLANKLINE>
discover_paths(directory: Union[pathlib.Path, str], pattern: str) -> List[pathlib.Path]
    Return a list of Paths within the given directory that match the given
    pattern.
<BLANKLINE>
    Args:
        directory: the directory in which is searched for paths.
        pattern: a pattern (example: '**/*.py').
<BLANKLINE>
    Returns: a list of Path objects.
<BLANKLINE>


```

## ❄ (Not So) Frequently Asked Questions
1) > When is Barentsz particularly useful?

    _When e.g. adding a class to some package and you want it to be picked up 
    in your application, without having to add an import or registration 
    somewhere._

2) > Does Barentsz require my classes to be compromised (e.g. with inheritance or a decorator or something)?

    _No, never._

3) > What must I do for Barentsz to discover my class (or function, attribute, etc.)?

    _Nothing special. Just make sure that the path that is explored is a Python package._

4) > Why do the "Help documentation" sections contain this "\<BLANKLINE\>"?

    _That's because this documentation is under [doctest](https://docs.python.org/3/library/doctest.html).
    It helps to ensure that the documentation is always up to date._

5) > What's with the funny name?

    _Well... since this library is all about exploring and discovering and because
    I really enjoyed the cold north, I thought it to be a fitting name._

## ❄ Changelist

### 1.0.0 [2020-07-28]
* First release. 🎉
