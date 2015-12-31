"""
SkCode cosmetics replacement utility code.
"""

import re

from .walketree import walk_tree_for_cls


DEFAULT_COSMETICS_MAP = (
    (re.compile(r'(\s+)---(\s+)'), r'\1—\2'),
    (re.compile(r'(\s+)--(\s+)'),  r'\1—\2'),
    (re.compile(r'\.\.\.'), r'…'),
    (re.compile(r'\(tm\)'), r'™'),
)


def setup_cosmetics_replacement(document_tree, cosmetics_map=DEFAULT_COSMETICS_MAP):
    """
    Setup the document for cosmetics replacement.
    :param document_tree: The document tree instance.
    :param cosmetics_map: A list of tuple with two values (compiled_regex, replacement_str).
    """

    # Inject options in all tree node requiring them
    for tree_node in walk_tree_for_cls(document_tree, object):
        if getattr(tree_node.opts, 'inject_cosmetic_options', False):
            setattr(tree_node.opts, 'cosmetics_map', cosmetics_map)


def do_cosmetics_replacement(input_text, options):
    """
    Do all cosmetics replacement.
    :param input_text: The input text to be processed.
    :param options: The current tag options class (used as storage class by the ``setup_cosmetics_replacement`` function).
    :return: The string with all cosmetics replacement done.
    """

    # Get the cosmetics map from the options container
    cosmetics_map = getattr(options, 'cosmetics_map', [])

    # Process all cosmetics
    output_text = input_text
    for regex, replacement in cosmetics_map:
        output_text = regex.sub(replacement, output_text)

    # Return the result
    return output_text
