"""
SkCode cosmetics replacement utility code.
"""

import re


# Default cosmetics replacement map (compiled regex)
DEFAULT_COSMETICS_MAP = (
    (re.compile(r'(\s+)---(\s+)'), r'\1—\2'),
    (re.compile(r'(\s+)--(\s+)'),  r'\1—\2'),
    (re.compile(r'\.\.\.'), r'…'),
    (re.compile(r'\(tm\)'), r'™'),
)

# Document attribute name for storing the base URL
COSMETICS_MAP_ATTR_NAME = 'COSMETICS_MAP'


def setup_cosmetics_replacement(document_tree, cosmetics_map=DEFAULT_COSMETICS_MAP):
    """
    Setup the document for cosmetics replacement.
    :param document_tree: The document tree instance to be setup.
    :param cosmetics_map: A tuple of tuple with two values ``(compiled_regex, replacement_str)``.
    """
    assert document_tree, "Document tree is mandatory."
    assert document_tree.is_root, "Document tree must be a root tree node instance."

    # Inject cosmetics map into the document attributes
    document_tree.attrs[COSMETICS_MAP_ATTR_NAME] = cosmetics_map or ()


def do_cosmetics_replacement(root_tree_node, input_text):
    """
    Do all cosmetics replacement.
    :param root_tree_node: The root tree node instance.
    :param input_text: The input text to be processed.
    :return: The input text with all cosmetics replacement done.
    """

    # Shortcut if not text
    if not input_text:
        return ''

    # Get the cosmetics map from the options container
    cosmetics_map = root_tree_node.attrs.get(COSMETICS_MAP_ATTR_NAME, ())

    # Process all cosmetics
    output_text = input_text
    for regex, replacement in cosmetics_map:
        output_text = regex.sub(replacement, output_text)

    # Return the result
    return output_text
