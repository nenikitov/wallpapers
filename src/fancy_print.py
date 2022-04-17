from enum import Enum
from colorama import Fore, Style, init as colorama_init


class MessageType(Enum):
    NORMAL = {
        'top'    : None,
        'bottom' : None,
        'left'   : None,
        'right'  : None,
        'spacing': 0,
        'style'  : [ ]
    }
    HEADER = {
        'top'    : '#',
        'bottom' : '#',
        'left'   : '### ',
        'right'  : ' ###',
        'spacing': 2,
        'style'  : [ Fore.GREEN ]
    }
    SECTION = {
        'top'    : None,
        'bottom' : None,
        'left'   : '=== ',
        'right'  : ' ===',
        'spacing': 1,
        'style'  : [ Fore.CYAN ]
    }
    INFO = {
        'top'    : None,
        'bottom' : None,
        'left'   : '@ ',
        'right'  : None,
        'spacing': 0,
        'style'  : [ Fore.BLUE ]
    }
    SUCCESS = {
        'top'    : None,
        'bottom' : None,
        'left'   : ':) ',
        'right'  : None,
        'spacing': 0,
        'style'  : [ Style.BRIGHT, Fore.GREEN ]
    }
    WARNING = {
        'top'    : None,
        'bottom' : '-',
        'left'   : '> ',
        'right'  : ' <',
        'spacing': 0,
        'style'  : [ Style.BRIGHT, Fore.YELLOW ]
    }
    ERROR = {
        'top'    : None,
        'bottom' : '-',
        'left'   : '! ',
        'right'  : ' !',
        'spacing': 0,
        'style'  : [ Style.BRIGHT, Fore.RED ]
    }


def fancy_print(message, type=MessageType.NORMAL, indent=0):
    t = type.value
    space = ' ' * 2 * indent
    left = t['left'] if t['left'] else ''
    right = t['right'] if t['right'] else ''
    text = f'{left}{message}{right}'

    # Set the style
    colorama_init()
    print(Style.RESET_ALL, end='')
    print(''.join(t['style']), end='')

    # Add spacing
    print('\n' * t['spacing'], end='')

    # Top
    if t['top']:
        print(space + t['top'] * len(text))
    # Middle
    print(space + text)
    # Bottom
    if t['bottom']:
        print(space + t['bottom'] * len(text))

    # Reset style
    print(Style.RESET_ALL, end='')
