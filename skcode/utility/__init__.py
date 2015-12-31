"""
SkCode utilities library.
"""

# Auto paragraphs utilities
from .paragraphs import (PARAGRAPH_NODE_NAME,
                         ParagraphTagOptions,
                         make_paragraphs)

# Cosmetics replacement utility
from .cosmetics import setup_cosmetics_replacement

# Smileys replacement utility
from .smileys import setup_smileys_replacement

# TODO replace links utility

# Footnotes utilities
from .footnotes import (extract_footnotes,
                        render_footnotes_html,
                        render_footnotes_text)

# Acronyms utilities
from .acronyms import extract_acronyms

# Titles utilities
from .titles import (extract_titles,
                     make_titles_hierarchy,
                     make_auto_title_ids)

# TODO extract figures utility, plus auto ID generation
