"""
SkCode titles utility code.
"""

from html import escape as escape_html

from .walketree import walk_tree_for_cls
from ..tags.titles import TitleTagOptions
from ..tools import slugify


def extract_titles(document_tree,
                   title_ops_cls=TitleTagOptions):
    """
    Extract all titles present in the given document tree.
    :param document_tree: The document tree to be analyzed.
    :param title_ops_cls: The options class used for title declarations.
    :return: A list of all titles node instances in the document.
    """
    assert document_tree, "Document tree is mandatory."
    # TODO Replace *_cls with the new categories based system

    # List of titles found
    titles = []

    # For each title declaration
    for tree_node in walk_tree_for_cls(document_tree, title_ops_cls):

        # Store the title entry
        titles.append(tree_node)

    # Return the list
    return titles


def make_titles_hierarchy(titles, level=1):
    """
    Turn a flat list of titles into a hierarchical nested set of titles and sub titles.
    Handle incorrectly nested title levels by using a best-effort algorithm.
    This function is a generator, inner sets are also generators.

    Example of input titles list (semantic code, not actual code):
        Title(id, level)
        (
            Title('A', 3),
            Title('B', 4),
            Title('C', 1),
            Title('D', 2),
            Title('E', 3),
            Title('F', 2),
            Title('G', 3),
            Title('H', 1),
            Title('I', 2),
            Title('J', 1),
            Title('K', 1),
            Title('L', 3),
            Title('M', 4),
            Title('N', 2),
        )

    And output (semantic code, not actual code):
        Title(id, level)
        [
            (Title('A', 3), [
                (Title('B', 4), [])
            ]),
            (Title('C', 1), [
                (Title('D', 2), [
                    (Title('E', 3), [])
                ]),
                (Title('F', 2), [
                    (Title('G', 3), [])
                ])
            ]),
            (Title('H', 1), [
                (Title('I', 2), [])
            ]),
            (Title('J', 1), []),
            (Title('K', 1), [
                (Title('L', 3), [
                    (Title('M', 4), [])
                ]), (Title('N', 2), [])
            ])
        ]

    :param titles: A list of all titles node instances.
    :param level: The current title level (1..6).
    :return: A nested list of titles, nested according to each title level.
    """
    assert 6 >= level > 0, "The title level must be in range 1..6 (included)."

    # Recursion stop condition
    if not titles:
        return []

    # Current titles group
    parent_title = None
    subtitles = []

    # For each title
    for title in titles:

        # Get the title level
        title_level = title.opts.title_level

        # If level match current target level
        if title_level == level:

            # Yield any currently available subtitles
            if subtitles and parent_title is not None:
                yield parent_title, make_titles_hierarchy(subtitles, level + 1)
            elif subtitles and parent_title is None:
                yield from make_titles_hierarchy(subtitles, level + 1)
            elif parent_title is not None:
                yield parent_title, []

            # Reset the current titles group
            parent_title = title
            subtitles = []

        else:

            # Add title to the current group
            subtitles.append(title)

    # Yield remaining titles
    if subtitles and parent_title is not None:
        yield parent_title, make_titles_hierarchy(subtitles, level + 1)
    elif subtitles and parent_title is None:
        yield from make_titles_hierarchy(subtitles, level + 1)
    elif parent_title is not None:
        yield parent_title, []


def make_auto_title_ids(document_tree,
                        title_ops_cls=TitleTagOptions):
    """
    Assign an auto-generated ID to any titles without one.
    :param document_tree: The document tree to be analyzed.
    :param title_ops_cls: The options class used for title declarations.
    """
    assert document_tree, "Document tree is mandatory."

    # For each title declaration
    for tree_node in walk_tree_for_cls(document_tree, title_ops_cls):

        # Get the current title ID
        title_id = tree_node.opts.get_permalink_slug(tree_node)

        # Auto generate an ID if required
        if not title_id:

            # Slugify the raw content of the title to create the ID
            title_id = slugify(tree_node.get_raw_content())

            # Save the ID
            tree_node.attrs[tree_node.opts.slug_id_attr_name] = title_id


def _recursive_render_titles_html(title_groups, output, li_class_name, a_class_name, ul_class_name):
    """
    Recursive helper for HTML rendering of titles summary.
    :param title_groups: List of two elements: ``[title, subtitles (another list)]``.
    :param output: The output list of HTML elements.
    :param li_class_name: The CSS class name for the ``li`` element.
    :param a_class_name: The CSS class name for the ``a`` element.
    :param ul_class_name: The CSS class name for the ``ul`` element.
    """
    li_class = ' class="%s"' % li_class_name if li_class_name else ''
    a_class = ' class="%s"' % a_class_name if a_class_name else ''
    ul_class = ' class="%s"' % ul_class_name if ul_class_name else ''

    # Process all titles
    for title, subtitles in title_groups:

        # Get the title ID
        title_id = title.opts.get_permalink_slug(title)

        # Output the HTML list element for this title
        output.append('<li%s>' % li_class)
        output.append('<a href="#%s"%s>%s</a>' % (title_id, a_class, escape_html(title.get_raw_content())))
        if subtitles:
            output.append('<ul%s>' % ul_class)
            _recursive_render_titles_html(subtitles, output, li_class_name, a_class_name, ul_class_name)
            output.append('</ul>')
        output.append('</li>')


def render_titles_hierarchy_html(title_groups,
                                 root_ul_class_name='titles-summary',
                                 li_class_name='titles-summary-entry',
                                 a_class_name='titles-summary-link',
                                 ul_class_name='titles-summary-subentry'):
    """
    Render a titles hierarchy generated by ``make_titles_hierarchy`` to an HTML summary.
    :param title_groups: The titles hierarchy generated by ``make_titles_hierarchy``.
    :param root_ul_class_name: The class name to be used for the root ``ul`` element (default to 'titles-summary').
    :param li_class_name: The class name to be used for each ``li`` elements (default to 'titles-summary-entry').
    :param a_class_name: The class name to be used for each ``a`` elements (default to 'titles-summary-link').
    :param ul_class_name: The class name to be used for each nested ``ul`` elements (default to
    'titles-summary-subentry').
    :return: The title hierarchy as an HTML summary.
    """
    root_ul_class = ' class="%s"' % root_ul_class_name if root_ul_class_name else ''

    # Shortcut for empty summary
    if not title_groups:
        return ''

    # Recursive build of the summary
    output = ['<ul%s>' % root_ul_class]
    _recursive_render_titles_html(title_groups, output, li_class_name, a_class_name, ul_class_name)
    output.append('</ul>')

    # Return the summary as string
    return '\n'.join(output)


def _recursive_render_titles_text(title_groups, output, indent=0):
    """
    Recursive helper for text rendering of titles summary.
    :param title_groups: List of two elements: ``[title, subtitles (another list)]``.
    :param output: The output list of text elements.
    :param indent: The current indent level.
    """
    for title, subtitles in title_groups:

        # Output the text for this title
        output.append('%s %s' % ('#' * indent, title.get_raw_content().strip()))
        _recursive_render_titles_text(subtitles, output, indent + 1)


def render_titles_hierarchy_text(title_groups):
    """
    Render a titles hierarchy generated by ``make_titles_hierarchy`` to an text summary.
    :param title_groups: The titles hierarchy generated by ``make_titles_hierarchy``.
    :return: The title hierarchy as an text summary.
    """

    # Shortcut for empty summary
    if not title_groups:
        return ''

    # Recursive build of the summary
    output = []
    _recursive_render_titles_text(title_groups, output)

    # Return the summary as string
    return '\n'.join(output)
