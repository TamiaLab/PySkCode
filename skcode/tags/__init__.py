"""
SkCode tag definitions code.
"""

# Base classes
from .base import (TagOptions,
                   WrappingTagOptions,
                   InlineWrappingTagOptions)


# Import all tag definitions here
from .internal import (RootTagOptions,
                       TextTagOptions,
                       ErroneousTextTagOptions,
                       NewlineTagOptions,
                       HardNewlineTagOptions)
from .titles import TitleTagOptions
from .codeblocks import (CodeBlockTagOptions,
                         FixedCodeBlockTagOptions)
from .alerts import (AlertBoxTagOptions,
                     FixedAlertBoxTagOptions,
                     ALERT_TYPE_ERROR,
                     ALERT_TYPE_DANGER,
                     ALERT_TYPE_WARNING,
                     ALERT_TYPE_INFO,
                     ALERT_TYPE_SUCCESS,
                     ALERT_TYPE_NOTE,
                     ALERT_TYPE_QUESTION)
from .figures import (FigureDeclarationTagOptions,
                      FigureCaptionTagOptions)
from .footnotes import (FootnoteDeclarationTagOptions,
                        FootnoteReferenceTagOptions)
from .textformatting import (BoldTextTagOptions,
                             ItalicTextTagOptions,
                             StrikeTextTagOptions,
                             UnderlineTextTagOptions,
                             SubscriptTextTagOptions,
                             SupscriptTextTagOptions,
                             PreTextTagOptions,
                             CiteTextTagOptions,
                             InlineCodeTextTagOptions,
                             InlineSpoilerTextTagOptions,
                             KeyboardTextTagOptions,
                             HighlightTextTagOptions,
                             SmallTextTagOptions)
from .textalign import (CenterTextTagOptions,
                        LeftTextTagOptions,
                        RightTextTagOptions,
                        JustifyTextTagOptions)
from .textdirection import (DirectionTextTagOptions,
                            FixedDirectionTextTagOptions,
                            TEXT_DIR_LEFT_TO_RIGHT,
                            TEXT_DIR_RIGHT_TO_LEFT)
from .textmodifiers import (LowerCaseTextTagOptions,
                            UpperCaseTextTagOptions,
                            CapitalizeTextTagOptions)
from .textcolors import (ColorTextTagOptions,
                         FixedColorTextTagOptions)
from .spoiler import SpoilerTagOptions
from .lists import (ListTagOptions,
                    UnorderedListTagOptions,
                    OrderedListTagOptions,
                    ListElementTagOptions)
from .todolists import (TodoListTagOptions,
                        TodoTaskTagOptions)
from .definitions import (DefinitionListTagOptions,
                          DefinitionListTermTagOptions,
                          DefinitionListTermDefinitionTagOptions)
from .tables import (TableTagOptions,
                     TableRowTagOptions,
                     TableHeaderCellTagOptions,
                     TableCellTagOptions)
from .webspecials import (HorizontalLineTagOptions,
                          LineBreakTagOptions,
                          CutHereTagOptions)
from .quotes import QuoteTagOptions
from .acronyms import AcronymTagOptions
from .links import (UrlLinkTagOptions,
                    EmailLinkTagOptions,
                    AnchorTagOptions,
                    GoToAnchorTagOptions)
from .medias import (ImageTagOptions,
                     YoutubeTagOptions)
from .electronic import NotNotationTagOptions
from .internalspecials import NoParseTagOptions
from .notabene import NotaBeneTagOptions
from .postscriptum import PostScriptumTagOptions


# Default list of recognized tags
DEFAULT_RECOGNIZED_TAGS_LIST = (
    
    # --- Titles
    TitleTagOptions(1),
    TitleTagOptions(2),
    TitleTagOptions(3),
    TitleTagOptions(4),
    TitleTagOptions(5),
    TitleTagOptions(6),

    # --- Code blocks
    CodeBlockTagOptions(),  # OK
    FixedCodeBlockTagOptions('python'),
    FixedCodeBlockTagOptions('cpp'),
    FixedCodeBlockTagOptions('java'),
    FixedCodeBlockTagOptions('html'),
    FixedCodeBlockTagOptions('php'),

    # --- Alerts box
    AlertBoxTagOptions(),
    FixedAlertBoxTagOptions(ALERT_TYPE_ERROR),
    FixedAlertBoxTagOptions(ALERT_TYPE_DANGER),
    FixedAlertBoxTagOptions(ALERT_TYPE_WARNING),
    FixedAlertBoxTagOptions(ALERT_TYPE_INFO),
    FixedAlertBoxTagOptions(ALERT_TYPE_SUCCESS),
    FixedAlertBoxTagOptions(ALERT_TYPE_NOTE),
    FixedAlertBoxTagOptions(ALERT_TYPE_QUESTION),

    # --- Text formatting
    BoldTextTagOptions(),
    ItalicTextTagOptions(),
    StrikeTextTagOptions(),
    UnderlineTextTagOptions(),
    SubscriptTextTagOptions(),
    SupscriptTextTagOptions(),
    PreTextTagOptions(),
    InlineCodeTextTagOptions(),
    InlineSpoilerTextTagOptions(),
    KeyboardTextTagOptions(),
    HighlightTextTagOptions(),
    SmallTextTagOptions(),
    # imath  # TODO
    CiteTextTagOptions(),

    # --- Text alignment
    CenterTextTagOptions(),
    LeftTextTagOptions(),
    RightTextTagOptions(),
    JustifyTextTagOptions(),

    # --- Text direction
    DirectionTextTagOptions(),
    FixedDirectionTextTagOptions(TEXT_DIR_LEFT_TO_RIGHT),
    FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT),

    # --- Text modifiers
    LowerCaseTextTagOptions(),
    UpperCaseTextTagOptions(),
    CapitalizeTextTagOptions(),

    # --- Text color
    ColorTextTagOptions(),
    FixedColorTextTagOptions('black'),
    FixedColorTextTagOptions('blue'),
    FixedColorTextTagOptions('gray'),
    FixedColorTextTagOptions('green'),
    FixedColorTextTagOptions('orange'),
    FixedColorTextTagOptions('purple'),
    FixedColorTextTagOptions('red'),
    FixedColorTextTagOptions('white'),
    FixedColorTextTagOptions('yellow'),

    # --- Spoiler box
    SpoilerTagOptions(),

    # --- Figure and caption
    FigureDeclarationTagOptions(),
    FigureCaptionTagOptions(),

    # --- Lists
    ListTagOptions(),
    UnorderedListTagOptions(),
    OrderedListTagOptions(),
    ListElementTagOptions(),

    # --- TO.DO list
    TodoListTagOptions(),
    TodoTaskTagOptions(),

    # --- Definitions lists
    DefinitionListTagOptions(),
    DefinitionListTermTagOptions(),
    DefinitionListTermDefinitionTagOptions(),
    
    # --- Tables
    TableTagOptions(),
    TableRowTagOptions(),
    TableHeaderCellTagOptions(),
    TableCellTagOptions(),

    # --- Web special
    HorizontalLineTagOptions(),
    LineBreakTagOptions(),
    CutHereTagOptions(),

    # --- Quotes
    QuoteTagOptions(),

    # --- Footnotes
    FootnoteDeclarationTagOptions(),
    FootnoteReferenceTagOptions(),

    # --- Acronyms
    AcronymTagOptions(),

    # --- Links
    AnchorTagOptions(),
    GoToAnchorTagOptions(),
    UrlLinkTagOptions(),
    EmailLinkTagOptions(),

    # --- Medias
    ImageTagOptions(),
    YoutubeTagOptions(),

    # --- Special electronic
    NotNotationTagOptions(),

    # --- Special internal
    NoParseTagOptions(),

    # --- Nota Bene
    NotaBeneTagOptions(),

    # --- Post scriptum
    PostScriptumTagOptions(),
)


def build_recognized_tags_dict(tag_options_list):
    """
    Turn a list of tag options class instances into a dictionary of ``{tag_name: instance}``.

    This function exits for compatibility reasons between the old dictionary-based declaration style
    and the new list based declaration style.

    The new declaration style use tag name and alias name declaration directly in the options class.
    This allow simple filtering of allowed tags according to the user permission or settings.

    :param tag_options_list: The list of tag options class instances of all known tags.
    :return: A dictionary ``{tag_name: instance}`` with all tag name and alias registered as key.
    """
    recognized_tags_dict = {}

    # For each tag declaration
    for tag_options in tag_options_list:

        # Register the canonical tag name
        recognized_tags_dict[tag_options.canonical_tag_name] = tag_options

        # Register all aliases
        for alias_name in tag_options.alias_tag_names:
            recognized_tags_dict[alias_name] = tag_options

    # Return the dict
    return recognized_tags_dict


# Old dict declaration style for backward compatibility
DEFAULT_RECOGNIZED_TAGS = build_recognized_tags_dict(DEFAULT_RECOGNIZED_TAGS_LIST)
