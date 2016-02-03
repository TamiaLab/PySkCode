"""
SkCode utilities library.
"""

# Auto paragraphs utility
from .paragraphs import make_paragraphs

# Cosmetics replacement utility
from .cosmetics import setup_cosmetics_replacement

# Smileys replacement utility
from .smileys import setup_smileys_replacement

# Relative to absolute URLs utility
from .relative_urls import setup_relative_urls_conversion

# Footnotes utilities
from .footnotes import (extract_footnotes,
                        render_footnotes_html,
                        render_footnotes_text)

# Acronyms utilities
from .acronyms import extract_acronyms

# Titles utilities
from .titles import (extract_titles,
                     make_titles_hierarchy,
                     make_auto_title_ids,
                     render_titles_hierarchy_html,
                     render_titles_hierarchy_text)

# figures utilities
from .figures import extract_figures
