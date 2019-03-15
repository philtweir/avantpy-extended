"""Creates a version of traceback.rst to insert in the documentation.

This assumes that such a file already exist; this is only done to
ensure we have the right destination. If so, we actually rewrite it.

"""

import os
import sys
from contextlib import redirect_stdout

this_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(this_dir, ".."))
sys.path.insert(0, this_dir)
sys.path.insert(0, parent_dir)

# sets up import hook; never used explicitly in code
import avantpy  # NOQA

assert avantpy  # silence pyflakes warnings about unused imports

target = os.path.normpath(os.path.join(parent_dir, "docs/source/tracebacks.rst"))

try:
    assert os.path.isfile(target)
except AssertionError:
    print("Wrong path: traceback.rst does not exist.")
    print("This program should be run from the root directory of this repository.")
    sys.exit()

content = """Friendly error messages
=======================

AvantPy aims to provide friendlier feedback when an exception is raised than what is
done by Python.
Such feedback will also be available in languages other than English.

.. note::

     The content of this file is generated by running
     update_tb.py located in the ``dev_tools`` directory,
     which needs to be done explicitly.
"""


def make_title(text):
    print(text)
    print("-" * len(text), "\n")


with open(target, "w") as out:
    with redirect_stdout(out):
        print(content)

        make_title("IfNobreakError")
        print("Example 1::")
        import ifnobreakerror  # NOQA

        assert ifnobreakerror  # silences pyflakes
