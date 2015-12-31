"""
SkCode (Python implementation of BBcode syntax) parser library.
"""

# Package information
__author__ = "Fabien Batteix (@skywodd)"
__copyright__ = "Copyright 2015, TamiaLab"
__credits__ = ["Fabien Batteix", "TamiaLab"]
__license__ = "GPLv3"
__version__ = "1.0.5"
__maintainer__ = "Fabien Batteix"
__email__ = "fabien.batteix@tamialab.fr"
__status__ = "Development"  # "Production"


# User friendly imports
from .treebuilder import parse_skcode
from .render import (render_to_html,
                     render_to_skcode,
                     render_to_text)
