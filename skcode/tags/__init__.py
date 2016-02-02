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
                          LineBreakTagOptions)
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


# Default list of recognized tags
DEFAULT_RECOGNIZED_TAGS = {
    
    # --- Titles
    'h1': TitleTagOptions(1),
    'h2': TitleTagOptions(2),
    'h3': TitleTagOptions(3),
    'h4': TitleTagOptions(4),
    'h5': TitleTagOptions(5),
    'h6': TitleTagOptions(6),

    # --- Code blocks
    'code': CodeBlockTagOptions(),
    'python': FixedCodeBlockTagOptions('python'),
    'cpp': FixedCodeBlockTagOptions('cpp'),
    'java': FixedCodeBlockTagOptions('java'),
    'html': FixedCodeBlockTagOptions('html'),
    'php': FixedCodeBlockTagOptions('php'),

    # --- Alerts box
    'alert': AlertBoxTagOptions(),
    'error': FixedAlertBoxTagOptions(ALERT_TYPE_ERROR),
    'danger': FixedAlertBoxTagOptions(ALERT_TYPE_DANGER),
    'warning': FixedAlertBoxTagOptions(ALERT_TYPE_WARNING),
    'info': FixedAlertBoxTagOptions(ALERT_TYPE_INFO),
    'success': FixedAlertBoxTagOptions(ALERT_TYPE_SUCCESS),
    'note': FixedAlertBoxTagOptions(ALERT_TYPE_NOTE),
    'question': FixedAlertBoxTagOptions(ALERT_TYPE_QUESTION),

    # --- Text formatting
    'b': BoldTextTagOptions(),
    'bold': BoldTextTagOptions(),
    'strong': BoldTextTagOptions(),
    
    'i': ItalicTextTagOptions(),
    'italic': ItalicTextTagOptions(),
    'em': ItalicTextTagOptions(),
    
    's': StrikeTextTagOptions(),
    'strike': StrikeTextTagOptions(),
    'del': StrikeTextTagOptions(),
    
    'u': UnderlineTextTagOptions(),
    'underline': UnderlineTextTagOptions(),
    'ins': UnderlineTextTagOptions(),
    
    'sub': SubscriptTextTagOptions(),
    'sup': SupscriptTextTagOptions(),
    'pre': PreTextTagOptions(),
    'icode': InlineCodeTextTagOptions(),
    'ispoiler': InlineSpoilerTextTagOptions(),
    
    'kbd': KeyboardTextTagOptions(),
    'keyboard': KeyboardTextTagOptions(),

    'glow': HighlightTextTagOptions(),
    'highlight': HighlightTextTagOptions(),
    'mark': HighlightTextTagOptions(),
    
    'small': SmallTextTagOptions(),
    
    # imath  # TODO
    'cite': CiteTextTagOptions(),

    # --- Text alignment
    'center': CenterTextTagOptions(),
    'left': LeftTextTagOptions(),
    'right': RightTextTagOptions(),
    'justify': JustifyTextTagOptions(),

    # --- Text direction
    'bdo': DirectionTextTagOptions(),
    'ltr': FixedDirectionTextTagOptions(TEXT_DIR_LEFT_TO_RIGHT),
    'rtl': FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT),

    # --- Text modifiers
    'lowercase': LowerCaseTextTagOptions(),
    'uppercase': UpperCaseTextTagOptions(),
    'capitalize': CapitalizeTextTagOptions(),

    # --- Text color
    'color': ColorTextTagOptions(),
    'black': FixedColorTextTagOptions('black'),
    'blue': FixedColorTextTagOptions('blue'),
    'gray': FixedColorTextTagOptions('gray'),
    'green': FixedColorTextTagOptions('green'),
    'orange': FixedColorTextTagOptions('orange'),
    'purple': FixedColorTextTagOptions('purple'),
    'red': FixedColorTextTagOptions('red'),
    'white': FixedColorTextTagOptions('white'),
    'yellow': FixedColorTextTagOptions('yellow'),

    # --- Spoiler box
    'hide': SpoilerTagOptions(),
    'spoiler': SpoilerTagOptions(),

    # --- Figure and caption
    'figure': FigureDeclarationTagOptions(),
    'figcaption': FigureCaptionTagOptions(),

    # --- Lists
    'list': ListTagOptions(),  # TODO better text version
    'ul': UnorderedListTagOptions(),
    'ol': OrderedListTagOptions(),
    'li': ListElementTagOptions(),
    
    # --- TO.DO list
    'todolist': TodoListTagOptions(),
    'task': TodoTaskTagOptions(),

    # --- Definitions lists
    'dl': DefinitionListTagOptions(),  # TODO better text version
    'dt': DefinitionListTermTagOptions(),
    'dd': DefinitionListTermDefinitionTagOptions(),
    
    # --- Tables
    'table': TableTagOptions(),  # TODO text version
    'tr': TableRowTagOptions(),
    'th': TableHeaderCellTagOptions(),
    'td': TableCellTagOptions(),

    # --- Web special
    'hr': HorizontalLineTagOptions(),
    'br': LineBreakTagOptions(),

    # --- Quotes
    'quote': QuoteTagOptions(),
    'blockquote': QuoteTagOptions(),

    # --- Footnotes
    'footnote': FootnoteDeclarationTagOptions(),
    'fn': FootnoteDeclarationTagOptions(),
    'fnref': FootnoteReferenceTagOptions(),

    # --- Acronyms
    'abbr': AcronymTagOptions(),
    'acronym': AcronymTagOptions(),

    # --- Links
    'anchor': AnchorTagOptions(),
    'goto': GoToAnchorTagOptions(),
    'url': UrlLinkTagOptions(),
    'link': UrlLinkTagOptions(),
    'email': EmailLinkTagOptions(),

    # --- Medias
    'img': ImageTagOptions(),
    'youtube': YoutubeTagOptions(),

    # --- Special electronic
    'not': NotNotationTagOptions(),

    # --- Special internal
    'nobbc': NoParseTagOptions(),
    'noparse': NoParseTagOptions(),
}
