"""
SkCode titles utility code.
"""

from .walketree import walk_tree_for_cls
from ..tags.titles import TitleTagOptions
from ..tools import slugify


def extract_titles(document_tree,
                   title_ops_cls=TitleTagOptions):
    """
    Extract all titles present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param title_ops_cls: The options class used for title declarations.
    :return: A nested list like [(title_id, title_node, title_level), ] of
    all titles node instances in the document.
    """

    # Map like [(title_id, title_node, title_level), ] of titles found
    titles = []

    # For each title declaration
    for tree_node in walk_tree_for_cls(document_tree, title_ops_cls):

        # Get the title ID and level
        title_id = tree_node.opts.get_permalink_slug(tree_node)
        title_level = tree_node.opts.title_level

        # Store the title entry
        titles.append((title_id, tree_node, title_level))

    # Return the map
    return titles


def make_titles_hierarchy(titles, level=1):
    """
    Turn a flat list of titles into a hierarchical nested set of titles and sub titles.
    Handle incorrectly nested title levels by using a best-effort algorithm.
    This function is a generator, inner sets are also generators.

    Example of input titles list:
        (
            ('A', None, 3),
            ('B', None, 4),
            ('C', None, 1),
            ('D', None, 2),
            ('E', None, 3),
            ('F', None, 2),
            ('G', None, 3),
            ('H', None, 1),
            ('I', None, 2),
            ('J', None, 1),
            ('K', None, 1),
            ('L', None, 3),
            ('M', None, 4),
            ('N', None, 2),
        )

    And output:
        [
            (('A', None, 3), [
                (('B', None, 4), [])
            ]),
            (('C', None, 1), [
                (('D', None, 2), [
                    (('E', None, 3), [])
                ]),
                (('F', None, 2), [
                    (('G', None, 3), [])
                ])
            ]),
            (('H', None, 1), [
                (('I', None, 2), [])
            ]),
            (('J', None, 1), []),
            (('K', None, 1), [
                (('L', None, 3), [
                    (('M', None, 4), [])
                ]), (('N', None, 2), [])
            ])
        ]

    Example of (recursive) display function:
        def _recur_print(title_groups, indent=0):
            for parent_title, sub_titles in title_groups:
                title_id, tree_node, title_level = parent_title
                print(' ' * 4 * indent, title_id, title_level)
                _recur_print(sub_titles, indent + 1)

    :param titles: A nested list like [(title_id, title_node, title_level), ] of all titles node instances.
    :return: A nested list of titles, nested according to each title level.
    """

    # Recursion stop condition
    if not titles:
        return []

    # Current titles group
    parent_title = None
    sub_titles = []

    # For each title
    for title in titles:

        # Unpack the title
        title_id, tree_node, title_level = title

        # If level match current target level
        if title_level == level:

            # Yield any currently available subtitles
            if sub_titles and parent_title is not None:
                yield parent_title, make_titles_hierarchy(sub_titles, level + 1)
            elif sub_titles and parent_title is None:
                for group in make_titles_hierarchy(sub_titles, level + 1):
                    yield group
            elif parent_title is not None:
                yield parent_title, []

            # Reset the current titles group
            parent_title = title
            sub_titles = []

        else:

            # Add title to the current group
            sub_titles.append(title)

    # Yield remaining titles
    if sub_titles and parent_title is not None:
        yield parent_title, make_titles_hierarchy(sub_titles, level + 1)
    elif sub_titles and parent_title is None:
        for group in make_titles_hierarchy(sub_titles, level + 1):
            yield group
    elif parent_title is not None:
        yield parent_title, []


def make_auto_title_ids(document_tree,
                        title_ops_cls=TitleTagOptions):

    # For each title declaration
    for tree_node in walk_tree_for_cls(document_tree, title_ops_cls):

        # Get the current title ID
        title_id = tree_node.opts.get_permalink_slug(tree_node)

        # Auto generate an ID if required
        if not title_id:
            title_id = slugify(tree_node.get_raw_content())

            # Save the ID
            tree_node.attrs[tree_node.opts.slug_id_attr_name] = title_id
