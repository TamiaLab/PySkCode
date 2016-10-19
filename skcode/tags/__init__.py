"""
SkCode tag definitions code.
"""

# Import all tag definitions here
from .internal import (
    TextTreeNode,
    NewlineTreeNode,
    HardNewlineTreeNode
)
from .titles import generate_title_cls
from .codeblocks import (
    CodeBlockTreeNode,
    generate_fixed_code_block_type_cls
)
from .alerts import (
    AlertBoxTreeNode,
    generate_fixed_alert_type_cls,
    ALERT_TYPE_ERROR,
    ALERT_TYPE_DANGER,
    ALERT_TYPE_WARNING,
    ALERT_TYPE_INFO,
    ALERT_TYPE_SUCCESS,
    ALERT_TYPE_NOTE,
    ALERT_TYPE_QUESTION
)
from .figures import (
    FigureDeclarationTreeNode,
    FigureCaptionTreeNode
)
from .footnotes import (
    FootnoteDeclarationTreeNode,
    FootnoteReferenceTreeNode
)
from .textformatting import (
    BoldTextTreeNode,
    ItalicTextTreeNode,
    StrikeTextTreeNode,
    UnderlineTextTreeNode,
    SubscriptTextTreeNode,
    SupscriptTextTreeNode,
    PreTextTreeNode,
    CiteTextTreeNode,
    InlineCodeTextTreeNode,
    InlineSpoilerTextTreeNode,
    KeyboardTextTreeNode,
    HighlightTextTreeNode,
    SmallTextTreeNode
)
from .textalign import (
    CenterTextTreeNode,
    LeftTextTreeNode,
    RightTextTreeNode,
    JustifyTextTreeNode
)
from .textdirection import (
    DirectionTextTreeNode,
    LTRFixedDirectionTextTreeNode,
    RTLFixedDirectionTextTreeNode
)
from .textmodifiers import (
    LowerCaseTextTreeNode,
    UpperCaseTextTreeNode,
    CapitalizeTextTreeNode
)
from .textcolors import (
    ColorTextTreeNode,
    generate_fixed_color_text_cls
)
from .spoiler import SpoilerTreeNode
from .lists import (
    ListTreeNode,
    UnorderedListTreeNode,
    OrderedListTreeNode,
    ListElementTreeNode
)
from .todolists import (
    TodoListTreeNode,
    TodoTaskTreeNode
)
from .definitions import (
    DefinitionListTreeNode,
    DefinitionListTermTreeNode,
    DefinitionListTermDefinitionTreeNode
)
from .tables import (
    TableTreeNode,
    TableRowTreeNode,
    TableHeaderCellTreeNode,
    TableCellTreeNode
)
from .webspecials import (
    HorizontalLineTreeNode,
    LineBreakTreeNode,
    CutHereTreeNode
)
from .quotes import QuoteTreeNode
from .acronyms import AcronymTreeNode
from .links import (
    UrlLinkTreeNode,
    EmailLinkTreeNode,
    AnchorTreeNode,
    GoToAnchorTreeNode
)
from .medias import (
    ImageTreeNode,
    YoutubeTreeNode
)
from .electronic import NotNotationTreeNode
from .internalspecials import NoParseTreeNode
from .notabene import NotaBeneTreeNode
from .postscriptum import PostScriptumTreeNode


# Default list of recognized tags
DEFAULT_RECOGNIZED_TAGS_LIST = (
    
    # --- Titles
    generate_title_cls(1),
    generate_title_cls(2),
    generate_title_cls(3),
    generate_title_cls(4),
    generate_title_cls(5),
    generate_title_cls(6),

    # --- Code blocks
    CodeBlockTreeNode,
    generate_fixed_code_block_type_cls('python'),
    generate_fixed_code_block_type_cls('cpp'),
    generate_fixed_code_block_type_cls('java'),
    generate_fixed_code_block_type_cls('html'),
    generate_fixed_code_block_type_cls('php'),

    # --- Alerts box
    AlertBoxTreeNode,
    generate_fixed_alert_type_cls(ALERT_TYPE_ERROR),
    generate_fixed_alert_type_cls(ALERT_TYPE_DANGER),
    generate_fixed_alert_type_cls(ALERT_TYPE_WARNING),
    generate_fixed_alert_type_cls(ALERT_TYPE_INFO),
    generate_fixed_alert_type_cls(ALERT_TYPE_SUCCESS),
    generate_fixed_alert_type_cls(ALERT_TYPE_NOTE),
    generate_fixed_alert_type_cls(ALERT_TYPE_QUESTION),

    # --- Text formatting
    BoldTextTreeNode,
    ItalicTextTreeNode,
    StrikeTextTreeNode,
    UnderlineTextTreeNode,
    SubscriptTextTreeNode,
    SupscriptTextTreeNode,
    PreTextTreeNode,
    InlineCodeTextTreeNode,
    InlineSpoilerTextTreeNode,
    KeyboardTextTreeNode,
    HighlightTextTreeNode,
    SmallTextTreeNode,
    CiteTextTreeNode,

    # --- Text alignment
    CenterTextTreeNode,
    LeftTextTreeNode,
    RightTextTreeNode,
    JustifyTextTreeNode,

    # --- Text direction
    DirectionTextTreeNode,
    LTRFixedDirectionTextTreeNode,
    RTLFixedDirectionTextTreeNode,

    # --- Text modifiers
    LowerCaseTextTreeNode,
    UpperCaseTextTreeNode,
    CapitalizeTextTreeNode,

    # --- Text color
    ColorTextTreeNode,
    generate_fixed_color_text_cls('black'),
    generate_fixed_color_text_cls('blue'),
    generate_fixed_color_text_cls('gray'),
    generate_fixed_color_text_cls('green'),
    generate_fixed_color_text_cls('orange'),
    generate_fixed_color_text_cls('purple'),
    generate_fixed_color_text_cls('red'),
    generate_fixed_color_text_cls('white'),
    generate_fixed_color_text_cls('yellow'),

    # --- Spoiler box
    SpoilerTreeNode,

    # --- Figure and caption
    FigureDeclarationTreeNode,
    FigureCaptionTreeNode,

    # --- Lists
    ListTreeNode,
    UnorderedListTreeNode,
    OrderedListTreeNode,
    ListElementTreeNode,

    # --- TO.DO list
    TodoListTreeNode,
    TodoTaskTreeNode,

    # --- Definitions lists
    DefinitionListTreeNode,
    DefinitionListTermTreeNode,
    DefinitionListTermDefinitionTreeNode,
    
    # --- Tables
    TableTreeNode,
    TableRowTreeNode,
    TableHeaderCellTreeNode,
    TableCellTreeNode,

    # --- Web special
    HorizontalLineTreeNode,
    LineBreakTreeNode,
    CutHereTreeNode,

    # --- Quotes
    QuoteTreeNode,

    # --- Footnotes
    FootnoteDeclarationTreeNode,
    FootnoteReferenceTreeNode,

    # --- Acronyms
    AcronymTreeNode,

    # --- Links
    AnchorTreeNode,
    GoToAnchorTreeNode,
    UrlLinkTreeNode,
    EmailLinkTreeNode,

    # --- Medias
    ImageTreeNode,
    YoutubeTreeNode,

    # --- Special electronic
    NotNotationTreeNode,

    # --- Special internal
    NoParseTreeNode,

    # --- Nota Bene
    NotaBeneTreeNode,

    # --- Post scriptum
    PostScriptumTreeNode,
)


def build_recognized_tags_dict(tag_class_list):
    """
    Turn a list of tag node classes into a dictionary of tag names and corresponding node class.
    :param tag_class_list: The list of tag node classes for all supported tags.
    :return: A dictionary ``{tag_name: class}`` with all tag name and alias registered as key.
    """
    recognized_tags_dict = {}

    # For each tag declaration
    for tag_class in tag_class_list:

        # Sanity checks
        if type(tag_class) is not type:
            raise ValueError('{} is an instance, not a class type.'.format(tag_class.__class__.__name__))
        if not tag_class.canonical_tag_name:
            raise ValueError('{} does not have a canonical name'.format(tag_class.__name__))

        # Register the canonical tag name
        if tag_class.canonical_tag_name in recognized_tags_dict:
            raise KeyError('Tag name "{}" is already registered'.format(tag_class.canonical_tag_name))
        recognized_tags_dict[tag_class.canonical_tag_name] = tag_class

        # Register all aliases
        for alias_name in tag_class.alias_tag_names:
            if alias_name in recognized_tags_dict:
                raise KeyError('Alias name "{}" is already registered'.format(alias_name))
            recognized_tags_dict[alias_name] = tag_class

    # Return the dict
    return recognized_tags_dict
