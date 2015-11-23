"""
SkCode utilities library.
"""

# Auto paragraphs utilities
from .paragraphs import (PARAGRAPH_NODE_NAME,
                         ParagraphTagOptions,
                         make_paragraphs)

# TODO replace cosmetic utility (maybe mixin for postrender callback instead?)
# TODO replace smiley utility (maybe mixin for postrender callback instead?)
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
