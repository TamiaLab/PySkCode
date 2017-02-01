"""
SkCode words count utility test code.
"""

import unittest

from skcode import parse_skcode
from skcode.utility.words_counter import count_words


class AcronymsUtilityTagTestCase(unittest.TestCase):
    """ Tests suite for the acronyms utility module. """

    def test_count_words(self):
        """ Test the ``count_words`` with no text """
        document = parse_skcode(
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Nulla eget erat sed nisi tincidunt pellentesque vel iaculis eros.
            In dui sapien, auctor et dui eget, elementum sodales justo.
            Fusce at condimentum magna, sed tincidunt lacus.
            [b]In quis scelerisque sem.[/b]

            [icode]This should NOT be count as text.[/icode]

            Phasellus congue, elit in dictum imperdiet, massa justo viverra libero, ac viverra nunc lectus vel turpis.
            Vestibulum placerat arcu quis sem euismod, at condimentum dui aliquam. Vivamus vitae cursus velit.
            [i]Praesent eget tempus lacus.[/i]

            Proin augue leo, consectetur ut risus gravida, varius cursus libero.
            Etiam lobortis iaculis elit, vel aliquam nibh rhoncus ut.
            Nunc auctor sapien vitae neque sodales congue. Suspendisse.""")
        words_count = count_words(document)
        self.assertEqual(100, words_count)
