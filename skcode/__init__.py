"""
PySkCode, a Python implementation of a full-featured BBCode syntax parser library.
"""

# Package information
__author__ = "Fabien Batteix (@skywodd)"
__copyright__ = "Copyright 2016, TamiaLab"
__credits__ = ["Fabien Batteix", "TamiaLab"]
__license__ = "GPLv3"
__version__ = "3.2.0"
__maintainer__ = "Fabien Batteix"
__email__ = "fabien.batteix@tamialab.fr"
__status__ = "Production"


# User friendly imports
from .treebuilder import parse_skcode
from .render import render_to_html, render_to_text
