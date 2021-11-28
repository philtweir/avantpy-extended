"""
TranslatedClass is a wrapper to translate the properties and methods of
a class using a dictionary.
"""

import yaml
import shutil
import os
import requests
from xdg import xdg_config_home, xdg_cache_home

RAW_GITHUB_PREFIX = 'https://raw.githubusercontent.com/philtweir/avantpy-extended/master/avantpy/wrappers/'

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
        v: module.__dict__[k]
        for k, v in
        translation_map.items()
        if k in module.__dict__
    })

def load_translations(yml, glbls, pkg):
    with open(yml, 'r') as f:
        mappings = yaml.safe_load(f)

    if 'coreMap' in mappings:
        global_translate(glbls, pkg, mappings['coreMap'])

    if 'classMap' in mappings:
        class_translate(pkg, mappings['coreMap'])

def class_translate(pkg, class_map):
    for cls, cls_def in class_map.items():
        if 'via' in cls_def:
            containing_pkg = __import__(cls_def['via'])
        else:
            containing_pkg = pkg
        soft_remap(pkg, cls, cls_def['map'])

def fetch_translations(translation_set, version=None):
    config_home = os.path.join(xdg_config_home(), 'avantpy-extended')
    cache_home = os.path.join(xdg_config_home(), 'avantpy-extended')

    # give precedence to local definitions
    development_version = os.path.join(
        os.path.dirname(__file__),
        f'{translation_set}.yaml'
    )
    if os.path.exists(development_version):
        return development_version

    if version is None:
        try:
            with open(os.path.join(config_home, '_index.yaml'), 'r') as f:
                index = yaml.safe_load(f)
        except IOError as e:
            os.makedirs(config_home, exist_ok=True)
            shutil.copy(os.path.join(os.path.dirname(__file__), '_index.yaml'), config_home)
            with open(os.path.join(config_home, '_index.yaml'), 'r') as f:
                index = yaml.safe_load(f)

        if translation_set not in index['packages']:
            return None

        translation_package_info = index['packages'][translation_set][-1]
        filename = f'{translation_set}-{translation_package_info["version"]}.yaml'
    else:
        filename = f'{translation_set}-{version}.yaml'

    location = os.path.join(cache_home, filename)
    if not os.path.exists(location):
        r = requests.get(RAW_GITHUB_PREFIX + filename)
        with open(location, 'w') as f:
            f.write(r.text)

    return location

def load_package(glbls, package):
    pkg = __import__(f'{package}__nt')
    translation_file = fetch_translations(package)
    load_translations(translation_file, glbls, pkg)
