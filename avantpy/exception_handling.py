"""Exception handling

Just a stub for now.

"""
import sys

from . import translate
from . import exceptions

DEBUG = False

ENABLED = True
def disable():
    '''Disables custom exception handling'''
    global ENABLED
    ENABLED = False

def _maybe_print(msg, obj, attribute):
    try:
        print(msg, getattr(object, attribute))
    except AttributeError:
        print(msg, "does not exist")


def get_partial_source(source, begin, end, mark=-1):
    """Extracts a few relevant lines from a source file"""

    lines = source.split("\n")
    result = []
    if mark == -1:
        mark = end

    for index, line in enumerate(lines, start=1):
        if index < begin:
            continue
        if index > end:
            break
        if index == mark:
            result.append("      -->{:5d}: ".format(index) + line)
        else:
            result.append("         {:5d}: ".format(index) + line)

    return "\n".join(result)


def handle_exception(exc, original_source):
    """Generic function to handle exceptions and return a
       friendlier traceback than Python.
    """
    if not ENABLED:
        # Let normal Python traceback through
        raise exc

    if DEBUG:
        print("\nInfo from sys")
        print("sys.exc_info(): ", sys.exc_info())
        _maybe_print("sys.last_type: ", sys, "last_type")
        _maybe_print("sys.last_value: ", sys, "last_value")
        _maybe_print("sys.last_traceback: ", sys, "last_traceback")

    name = exc.__class__.__name__
    if name in dispatch:
        return dispatch[name](exc, original_source)
        

    print("An exception was raised:")
    print("name: ", exc.__class__.__name__)
    print("args: ", exc.args)


def handle_IfNobreakError(exc, original_source):
    params = exc.args[0]

    if_linenumber = int(params["if_string"][1])
    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    if_line = lines[if_linenumber - 1]
    nobreak_line = lines[nobreak_linenumber - 1]
    partial_source = get_partial_source(
        original_source, 
        if_linenumber, 
        nobreak_linenumber
    )

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "partial_source": partial_source,
        "nobreak_linenumber": nobreak_linenumber
    }
    return translate.get('IfNobreakError', lang).format(**info)


def handle_TryNobreakError(exc, original_source):
    params = exc.args[0]

    try_linenumber = int(params["try_string"][1])
    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    try_line = lines[try_linenumber - 1]
    nobreak_line = lines[nobreak_linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "try_linenumber": try_linenumber,
        "try_line": try_line,
        "nobreak_linenumber": nobreak_linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('TryNobreakError', lang).format(**info)


def handle_NobreakSyntaxError(exc, original_source):
    params = exc.args[0]

    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    nobreak_line = lines[nobreak_linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "linenumber": nobreak_linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('NobreakSyntaxError', lang).format(**info)


def handle_NobreakFirstError(exc, original_source):
    params = exc.args[0]
    linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    nobreak_line = lines[linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "linenumber": linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('NobreakFirstError', lang).format(**info)


def handle_RepeatFirstError(exc, original_source):
    params = exc.args[0]
    linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    repeat_line = lines[linenumber - 1]

    info = {'filename': params["source_name"],
        "repeat_kwd": params["repeat keyword"],
        "linenumber": linenumber,
        "repeat_line": repeat_line
    }
    return translate.get('RepeatFirstError', lang).format(**info)


dispatch = {
    'IfNobreakError': handle_IfNobreakError,
    'TryNobreakError': handle_TryNobreakError,
    'NobreakFirstError': handle_NobreakFirstError,
    'NobreakSyntaxError': handle_NobreakSyntaxError,
    'RepeatFirstError': handle_RepeatFirstError,
}