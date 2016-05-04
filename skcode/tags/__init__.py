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
DEFAULT_RECOGNIZED_TAGS = {
    
    # --- Titles
    'h1': TitleTagOptions(1),  # OK
    'h2': TitleTagOptions(2),  # OK
    'h3': TitleTagOptions(3),  # OK
    'h4': TitleTagOptions(4),  # OK
    'h5': TitleTagOptions(5),  # OK
    'h6': TitleTagOptions(6),  # OK

    # --- Code blocks
    'code': CodeBlockTagOptions(),  # OK
    'python': FixedCodeBlockTagOptions('python'),  # OK
    'cpp': FixedCodeBlockTagOptions('cpp'),  # OK
    'java': FixedCodeBlockTagOptions('java'),  # OK
    'html': FixedCodeBlockTagOptions('html'),  # OK
    'php': FixedCodeBlockTagOptions('php'),  # OK

    # --- Alerts box
    'alert': AlertBoxTagOptions(), # OK
    'error': FixedAlertBoxTagOptions(ALERT_TYPE_ERROR),  # OK
    'danger': FixedAlertBoxTagOptions(ALERT_TYPE_DANGER),  # OK
    'warning': FixedAlertBoxTagOptions(ALERT_TYPE_WARNING),  # OK
    'info': FixedAlertBoxTagOptions(ALERT_TYPE_INFO),  # OK
    'success': FixedAlertBoxTagOptions(ALERT_TYPE_SUCCESS),  # OK
    'note': FixedAlertBoxTagOptions(ALERT_TYPE_NOTE),  # OK
    'question': FixedAlertBoxTagOptions(ALERT_TYPE_QUESTION),  # OK

    # --- Text formatting
    'b': BoldTextTagOptions(),  # OK
    'bold': BoldTextTagOptions(),  # OK
    'strong': BoldTextTagOptions(),  # OK
    
    'i': ItalicTextTagOptions(),  # OK
    'italic': ItalicTextTagOptions(),  # OK
    'em': ItalicTextTagOptions(),  # OK
    
    's': StrikeTextTagOptions(),  # OK
    'strike': StrikeTextTagOptions(),  # OK
    'del': StrikeTextTagOptions(),  # OK
    
    'u': UnderlineTextTagOptions(),  # OK
    'underline': UnderlineTextTagOptions(),  # OK
    'ins': UnderlineTextTagOptions(),  # OK
    
    'sub': SubscriptTextTagOptions(),  # OK
    'sup': SupscriptTextTagOptions(),  # OK
    'pre': PreTextTagOptions(),  # OK
    'icode': InlineCodeTextTagOptions(),  # OK
    'ispoiler': InlineSpoilerTextTagOptions(),  # OK
    
    'kbd': KeyboardTextTagOptions(),  # OK
    'keyboard': KeyboardTextTagOptions(),  # OK

    'glow': HighlightTextTagOptions(),  # OK
    'highlight': HighlightTextTagOptions(),  # OK
    'mark': HighlightTextTagOptions(),  # OK
    
    'small': SmallTextTagOptions(),  # OK
    
    # imath  # TODO
    'cite': CiteTextTagOptions(),  # OK

    # --- Text alignment
    'center': CenterTextTagOptions(),  # OK
    'left': LeftTextTagOptions(),  # OK
    'right': RightTextTagOptions(),  # OK
    'justify': JustifyTextTagOptions(),  # OK

    # --- Text direction
    'bdo': DirectionTextTagOptions(),  # OK
    'ltr': FixedDirectionTextTagOptions(TEXT_DIR_LEFT_TO_RIGHT),  # OK
    'rtl': FixedDirectionTextTagOptions(TEXT_DIR_RIGHT_TO_LEFT),  # OK

    # --- Text modifiers
    'lowercase': LowerCaseTextTagOptions(),  # OK
    'uppercase': UpperCaseTextTagOptions(),  # OK
    'capitalize': CapitalizeTextTagOptions(),  # OK

    # --- Text color
    'color': ColorTextTagOptions(),  # OK
    'black': FixedColorTextTagOptions('black'),  # OK
    'blue': FixedColorTextTagOptions('blue'),  # OK
    'gray': FixedColorTextTagOptions('gray'),  # OK
    'green': FixedColorTextTagOptions('green'),  # OK
    'orange': FixedColorTextTagOptions('orange'),  # OK
    'purple': FixedColorTextTagOptions('purple'),  # OK
    'red': FixedColorTextTagOptions('red'),  # OK
    'white': FixedColorTextTagOptions('white'),  # OK
    'yellow': FixedColorTextTagOptions('yellow'),  # OK

    # --- Spoiler box
    'hide': SpoilerTagOptions(),  # OK
    'spoiler': SpoilerTagOptions(),  # OK

    # --- Figure and caption
    'figure': FigureDeclarationTagOptions(),  # OK
    'figcaption': FigureCaptionTagOptions(),  # OK

    # --- Lists
    'list': ListTagOptions(),  # OK
    'ul': UnorderedListTagOptions(),  # OK
    'ol': OrderedListTagOptions(),  # OK
    'li': ListElementTagOptions(),  # OK
    '*': ListElementTagOptions(),  # OK

    # --- TO.DO list
    'todolist': TodoListTagOptions(),  # OK
    'task': TodoTaskTagOptions(),  # OK

    # --- Definitions lists
    'dl': DefinitionListTagOptions(),  # OK
    'dt': DefinitionListTermTagOptions(),  # OK
    'dd': DefinitionListTermDefinitionTagOptions(),  # OK
    
    # --- Tables
    'table': TableTagOptions(),  # OK
    'tr': TableRowTagOptions(),  # OK
    'th': TableHeaderCellTagOptions(),  # OK
    'td': TableCellTagOptions(),  # OK

    # --- Web special
    'hr': HorizontalLineTagOptions(),  # OK
    'br': LineBreakTagOptions(),  # OK
    'cuthere': CutHereTagOptions(),  # OK

    # --- Quotes
    'quote': QuoteTagOptions(),  # OK
    'blockquote': QuoteTagOptions(),  # OK

    # --- Footnotes
    'footnote': FootnoteDeclarationTagOptions(),  # OK
    'fn': FootnoteDeclarationTagOptions(),  # OK
    'fnref': FootnoteReferenceTagOptions(),  # OK

    # --- Acronyms
    'abbr': AcronymTagOptions(),  # OK
    'acronym': AcronymTagOptions(),  # OK

    # --- Links
    'anchor': AnchorTagOptions(),  # OK
    'goto': GoToAnchorTagOptions(),  # OK
    'url': UrlLinkTagOptions(),  # OK
    'link': UrlLinkTagOptions(),  # OK
    'email': EmailLinkTagOptions(),  # OK

    # --- Medias
    'img': ImageTagOptions(),  # OK
    'youtube': YoutubeTagOptions(),  # OK

    # --- Special electronic
    'not': NotNotationTagOptions(),  # OK

    # --- Special internal
    'nobbc': NoParseTagOptions(),  # OK
    'noparse': NoParseTagOptions(),  # OK

    # --- Nota Bene
    'notabene': NotaBeneTagOptions(),  # OK
    'nb': NotaBeneTagOptions(),  # OK

    # --- Post scriptum
    'postscriptum': PostScriptumTagOptions(),  # OK
    'ps': PostScriptumTagOptions(),  # OK
}
