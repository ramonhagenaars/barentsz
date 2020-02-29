from pathlib import Path
from unittest import TestCase

from barentsz._discover import discover_modules, _get_modules_from_source, _is_package
from test_resources.level2 import module1 as level2_module1


class TestDiscoverModules(TestCase):

    def test_discover_modules(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')
        expected_module0 = 'test_resources.module1'
        expected_module1 = 'test_resources.level2.module1'

        # EXECUTE
        modules = discover_modules(path_to_resources)
        module_names = [module.__name__ for module in modules]

        # VERIFY
        self.assertEqual(2, len(modules))
        self.assertIn(expected_module0, module_names)
        self.assertIn(expected_module1, module_names)

    def test_discover_modules_with_raise(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources')

        # EXECUTE & VERIFY
        with self.assertRaises(ImportError):
            # test_resources.level2.module2 has invalid syntax.
            discover_modules(path_to_resources, raise_on_fail=True)

    def test_get_modules_from_source(self):
        # SETUP
        path_to_resources = Path(__file__).parent.parent.joinpath('test_resources/level2')
        str_path_to_resources = str(path_to_resources)
        iterable_of_modules = [level2_module1]

        # EXECUTE
        a = _get_modules_from_source(path_to_resources)
        b = _get_modules_from_source(str_path_to_resources)
        c = _get_modules_from_source(level2_module1)
        d = _get_modules_from_source(iterable_of_modules)

        # VERIFY
        self.assertTrue(a == b == c == d)




    # if isinstance(source, Path):
    #     modules = discover_modules(source, in_private_modules, raise_on_fail)
    # elif isinstance(source, str):
    #     modules = discover_modules(Path(source), in_private_modules,
    #                                raise_on_fail)
    # elif isinstance(source, Module):
    #     modules = [source]
    # elif instance_of(source, Iterable[Module]):
    #     modules = source
    # else:
    #     raise ValueError('The given source must be a Path, string or module. '
    #                      'Given: {}'.format(source))