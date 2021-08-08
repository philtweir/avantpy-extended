"""
TranslatedClass is a wrapper to translate the properties and methods of
a class using a dictionary.
"""

class TranslatedClass:
    def __init__(self, factory, translation_map, *args, soft=False, **kwargs):
        self.__dict__['__translation_instance'] = factory(*args, **kwargs)
        self.__dict__['__translation_soft'] = soft
        self.__dict__['__translation_map'] = {
            v: k for (k, v) in translation_map.items()
        }

    def __setattr__(self, attr, val):
        if attr in self.__dict__['__translation_map']:
            attr = self.__dict__['__translation_map'][attr]
        elif not self.__dict__['__translation_soft']:
            raise AttributeError

        return setattr(self.__dict['__translation_instance'], attr)

    def __getattr__(self, attr):
        if attr in self.__dict__['__translation_map']:
            attr = self.__dict__['__translation_map'][attr]
        elif not self.__dict__['__translation_soft']:
            raise AttributeError

        return getattr(self.__dict__['__translation_instance'], attr)

    def __call__(self, *args, **kwargs):
        return self.__dict__['__translation_instance'].__call__(*args, **kwargs)

def soft_remap(module, factory_str, translation_map):
    original = getattr(module, factory_str)
    setattr(module, factory_str, lambda *args, **kwargs: TranslatedClass(original, translation_map, *args, soft=True, **kwargs))

def global_translate(globals, module, translation_map):
    globals.update({
        v: module.__dict__[k] for k, v in translation_map.items()
    })
