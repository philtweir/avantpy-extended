Bienvenue 환영합니다 Bienvenido - ようこそ Welcome  歡迎光臨
========================================================================

**AvantPy** - Python with training wheels: executable pseudocode in any language.


.. warning::

    This is pre-alpha software, currently in development.
    **Currently**, it is only tested from a local repository, and while it is
    available from pypi.org using pip, we do not test with such
    an installed version.


What is AvantPy?
----------------

- AvantPy is a collection of dialects, each dialect being a superset of Python, designed to make it easier to learn programming concepts in a given human language.

  - Each dialect consists of a translations of most Python keywords in a given human language, supplemented by a few additional constructs intended to make some programming concepts easier to learn.
  - The current version includes four dialects: English, French and Spanish, as
    well as an UPPERCASE version of the English dialect.
    The translation currently done in these three dialects is subject to change; feel free to make suggestions for alternative to use, or contribute a new dialect.

- AvantPy is a preprocessor, that takes a program written either totally or
  in parts in a given dialect, and converts it to standard Python prior to execution.

  - A syntactically valid program can include a mix of code written in normal Python and in a specific dialect. This is to ease the transition to learning Python.

- AvantPy is written as a standard Python module/package meant to be usable with any "normal" Python environment. Thus, it could be included as a plugin for a given
  editor, or run with a standard Python interpreter from the command line.
- AvantPy also includes a tool to convert programs written in a given dialect into standard Python, showing the differences between the two, thus helping motivated users to make the transition to using only standard Python.

  - It is also possible to translate valid programs from one dialect into another.

- AvantPy also includes a custom REPL that can use any of the existing dialects.

- Finally, AvantPy uses `friendly-traceback <https://aroberge.github.io/friendly-traceback-docs/docs/html/>`_ to analyze Python tracebacks and translate them into easier to understand feedback for beginners.


Who is it for?
---------------

The main target audience is composed of students who do not know English and
are learning programming for the first time, under the guidance of an
instructor. It can also be helpful for students making the transition from
block-based programming languages to text-based ones.


Executable pseudocode?
-------------------------

Python is often described as executable pseudocode. Once people have learned a few idiomatic expressions, like::

    for variable in range(n):

translating pseudocode written in English into Python is usually very straightforward.

If the pseudocode is not written in English, the translation process is, at least initially, not as straightforward since an additional mental step is required by the translation from the original language into Python's English.

Even though the number of Python keywords is small, for absolute beginners who are learning programming concepts (control flow structures, defining functions, etc.), being able to use a language that uses keywords easily understood in their own language can definitely facilitate the learning process.
**This is the approach taken by people using block-based environments
(Scratch, Blockly, etc.) developed by educational experts
to help students learn programming concepts.**

Realistically, many students who learn computer programming as part of a formal course might never use programming again or, if so, it might not be for many years.
As `Mark Guzdial wrote: <https://computinged.wordpress.com/2019/01/07/a-little-bit-of-computing-goes-a-long-way-the-sigcse-50th-anniversary-issue-of-acm-inroads/>`_

   *People code for different purposes, with different ways of appropriating code. ... Not everybody is going to be a professional software developer, and they don’t need to be.*

And, he also `wrote in a later blog post: <https://computinged.wordpress.com/2019/03/25/task-specific-programming-languages-past-guzdial-is-smarter-than-present-guzdial/>`_ something
I very much agree with:

   *If we want people to program, make it easy. Remove the barriers. That’s what we’re about.* [Note: I am using this quote in a different context than that of the blog post.]

Given enough time, beginners who have just learned programming and stop using it
would likely forget most of the programming syntax they had learned.
However I claim that they likely would understand and remember programming **concepts** better if they are first learning them in their native language.  This is what AvantPy aims to do for them.


Contents
--------

.. toctree::
   :maxdepth: 2

    Invocation <invocation>
    Language or dialect? <dialect>
    Guiding principles <principles>
    Special keyword: repeat <repeat>
    Special keyword: nobreak <nobreak>
    Special keyword: notimported <notimported>
    More than keywords <builtins>
    Friendly error messages <tracebacks_upper>
    How does it work? <works>
    Testing <testing>
    Other modules <modules>
    Contributing <contribute>
    Notes on translations <translations_notes>
    Friendly error messages - en Français <tracebacks_fr>


.. todolist::

