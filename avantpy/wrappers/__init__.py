from contextlib import contextmanager
from ._translated import TranslatedClass, TranslatedContextClass
from forbiddenfruit import curse

def remap_type(typ, typ_map):
    for k, v in typ_map.items():
        curse(typ, v, getattr(typ, k))

STR_MAP = {
    'strip': 'lomadh',
    'join': 'comhcheanglaíodh'
}
LIST_MAP = {
    'append': 'iarcheanglaíodh',
    'remove': 'baineadh'
}

remap_type(str, STR_MAP)
remap_type(list, LIST_MAP)

OPEN_MAP = {
    'readlines': 'léadhlínte'
}

open_orig = open
def open_tr(*args, **kwargs):
    return TranslatedContextClass(open_orig, OPEN_MAP, OPEN_MAP, *args, soft=True, **kwargs)

__builtins__['open'] = open_tr
