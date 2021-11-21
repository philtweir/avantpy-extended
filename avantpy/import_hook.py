"""A custom importer making use of the import hook capability
"""
import importlib
import yaml
import os
import os.path
import sys

from codeop import CommandCompiler
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

import friendly_traceback

from . import session
from . import converter
from .my_gettext import gettext_lang
from .wrappers._translated import global_translate, fetch_translations

MAIN_MODULE_NAME = None
COUNTER = 0

friendly_traceback.exclude_file_from_traceback(__file__)


def import_main(name):
    """Imports the module that is to be interpreted as the main module.

       avantpy is often invoked with a script meant to be run as the
       main module its source is transformed with the -s (or --source) option,
       as in::

           python -m avantpy -s name

       Python identifies avantpy as the main script, which is not what we want.
    """
    global MAIN_MODULE_NAME
    _ = gettext_lang.lang
    MAIN_MODULE_NAME = name
    try:
        main = importlib.import_module(name)
        return main
    except ModuleNotFoundError:
        print(_("Cannot find main module: "), name)


class AvantPyRenamerLoader(Loader):
    def __init__(self, loader, name, rename):
        self.loader = loader
        self.name = name
        self.rename = rename

    def create_module(self, spec):
        return super().create_module(spec)

    def exec_module(self, module):
        module.__name__ = self.rename
        mod = self.loader.exec_module(module)
        return mod

    def is_package(self, fullname):
        return self.loader.is_package(fullname.replace(self.name, self.rename))

class AvantPyMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def find_spec(self, fullname, path, target=None):
        """Finds the appropriate properties (spec) of a module, and sets
           its loader."""

        if not path:
            path = [os.getcwd(), os.path.join(os.path.dirname(__file__), 'wrappers')]
        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname

        top_level = fullname.split('.')[0]
        if top_level.endswith('__nt'):
            real_fullname = top_level[:-4] + fullname[len(top_level):]
            real_fullname = importlib.util.resolve_name(real_fullname, None)
            for finder in sys.meta_path[1:]:
                package = top_level[:-4] if '.' in fullname else None
                spec = finder.find_spec(real_fullname, package)
                if spec is not None:
                    break
            else:
                return None
            spec.name = fullname
            total = [top_level[:-4]] + fullname.split('.')[1:]
            rename = '.'.join(total)
            spec.loader = AvantPyRenamerLoader(spec.loader, fullname, rename)
            return spec

        for entry in path:
            exts = [session.state.get_dialect()]
            if None in exts:
                exts = session.state.all_dialects()
            for ext in exts:
                for filename in (name, fullname):
                    filename = fullname.split('.')
                    suffixes = list(filename)
                    for _ in filename:
                        info = fetch_translations(suffixes[0])
                        if info is not None and os.path.exists(info):
                            with open(info, 'r') as f:
                                dct = yaml.safe_load(f)
                                dct['translatedSubmodulesReverse'] = {
                                    v['mapTo'].split('.')[1]: k
                                    for k, v in dct['translatedSubmodules'].items()
                                }

                                if 'mapTo' in dct:
                                    if len(filename) > 1:
                                        if filename[1] in dct['translatedSubmodules']:
                                            submodule = dct['translatedSubmodules'][filename[1]]
                                            wrapped_name = submodule['mapTo']
                                            wrapped_package = wrapped_name.split('.')[0] + '__nt'
                                            total = [wrapped_package] + wrapped_name.split('.')[1:]
                                            wrapped_spec = importlib.util.find_spec('.'.join(total), wrapped_package)
                                            if wrapped_spec:
                                                spec = importlib.util.spec_from_loader(
                                                    fullname,
                                                    WrappingLoader(wrapped_name, wrapped_spec, submodule['coreMap'])
                                                )
                                                return spec
                                        elif filename[1] in dct['translatedSubmodulesReverse']:
                                            wrapped_package = filename[0] + '__nt'
                                            total = [wrapped_package] + filename[1:]
                                            wrapped_spec = importlib.util.find_spec('.'.join(total), wrapped_package)
                                            if wrapped_spec:
                                                spec = importlib.util.spec_from_loader(
                                                    '.'.join(filename),
                                                    WrappingLoader('.'.join(filename), wrapped_spec, {})
                                                )
                                                return spec
                        back = suffixes.pop()

                    filename[-1] += '.' + ext

                    filename = os.path.join(entry, *filename)
                    if os.path.exists(filename):
                        return spec_from_file_location(
                            fullname,
                            filename,
                            loader=AvantPyLoader(filename),
                            submodule_search_locations=None,
                        )
        return None  # Not an AvantPy file


sys.meta_path.insert(0, AvantPyMetaFinder())


class WrappingLoader(Loader):
    def __init__(self, wrapped_name, wrapped_spec, translation_dict):
        self.wrapped_spec = wrapped_spec
        self.wrapped_name = wrapped_name
        self.translation_dict = translation_dict
        super().__init__()

    def is_package(self, fullname):
        return self.wrapped_spec.parent == self.wrapped_spec.name

    def create_module(self, spec):
        module = importlib.util.module_from_spec(self.wrapped_spec)
        global_translate(module.__dict__, module, self.translation_dict)
        module.__dict__.update({
            k: module.__dict__[v]
            for k, v in
            self.translation_dict.items()
        })
        return module

    def exec_module(self, module):
        self.wrapped_spec.loader.exec_module(module)

class AvantPyLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(self, filename):
        self.filename = filename
        self.compile = CommandCompiler()

    def exec_module(self, module):
        """import the source code, converts it before executing it."""
        global COUNTER
        COUNTER += 1
        if module.__name__ == MAIN_MODULE_NAME:
            module.__name__ = "__main__"

        with open(self.filename, encoding="utf8") as f:
            source = f.read()
        # original = source

        _path, extension = os.path.splitext(self.filename)
        # name = os.path.basename(_path)
        # fullname = name + extension
        dialect = extension[1:]

        friendly_traceback.cache.add(self.filename, source)
        try:
            session.state.set_dialect(dialect)
            source = converter.convert(source, dialect, filename=self.filename)
        except Exception:
            friendly_traceback.explain()
            return

        # ------------------------
        # Previously, we did the following essentially in one step:
        #
        #     exec(source, vars(module))
        #
        # The problem with that approach is that exec() records '<string>'
        # as the filename, for every file thus loaded; in some cases, the
        # prevented the traceback from having access to the source of the file.
        # By doing it in two steps, as we do here by first using compile()
        # and then exec(), we ensure that the correct filename is attached
        # to the code objects.
        # -------------------------

        try:
            code_obj = compile(source, self.filename, "exec")
        except Exception:
            friendly_traceback.explain()

        try:
            exec(code_obj, vars(module))
        except Exception as e:
            friendly_traceback.explain()
        return
