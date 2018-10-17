import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

def format(color, style='', sec_style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if ('bold' in style) or ('bold' in sec_style):
        _format.setFontWeight(QFont.Bold)
    if ('italic' in style) or ('italic' in sec_style):
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'param': format('blue', 'bold','italic'),
    'ground': format('green', 'bold'),
    'mass': format('darkCyan', 'bold'),
    'mass_grav': format('cyan','bold'),
    'osc': format('magenta', 'bold'),
    'spring': format('blue', 'bold'),
    'nlSpring': format('darkBlue', 'bold'),
    'detent': format('darkMagenta', 'bold'),
    'nlPluck': format('darkRed', 'bold'),
    'nlBow': format('red', 'bold'),
    'comment': format('darkGreen', 'italic'),
    'numbers': format('brown'),
    'forceInput': format('purple','bold'),
    'posInput': format('purple','bold'),
    'posOutput': format('purple','bold', 'italic'),
    'frcOutput': format('purple','bold', 'italic'),
    'names': format('black','bold'),
}


class ModelHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for mass interaction physical models.
    """
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # All other rules
        rules += [
            # 'self'
            (r'\bparam\b', 0, STYLES['param']),
            (r'\bmass\b', 0, STYLES['mass']),
            (r'\bmassG\b', 0, STYLES['mass_grav']),
            (r'\bosc\b', 0, STYLES['osc']),
            (r'\bground\b', 0, STYLES['ground']),
            (r'\bspring\b', 0, STYLES['spring']),
            (r'\bnlSpring\b', 0, STYLES['nlSpring']),
            (r'\bdetent\b', 0, STYLES['detent']),
            (r'\bnlPluck\b', 0, STYLES['nlPluck']),
            (r'\bnlBow\b', 0, STYLES['nlBow']),
            (r'\bfrcInput\b', 0, STYLES['forceInput']),
            (r'\bposInput\b', 0, STYLES['posInput']),
            (r'\bposOutput\b', 0, STYLES['posOutput']),
            (r'\bfrcOutput\b', 0, STYLES['frcOutput']),

            (r'@[^ ]*', 0, STYLES['names']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]


    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
