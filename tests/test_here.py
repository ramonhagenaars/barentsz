from pathlib import Path
from unittest import TestCase

from barentsz import here


class TestHere(TestCase):

    def test_here(self):
        # EXECUTE
        this_dir = here()

        # VERIFY
        self.assertEqual(Path(__file__).parent, this_dir)
