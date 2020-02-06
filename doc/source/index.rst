rjgtoys.projects: A simple wrapper for setuptools
=================================================

Provides an alternative to the :func:`setuptools.setup` function
that defines a Python project.

This package is very specific to how I like to build projects, and
I doubt it will be of much use to anyone else.

I'm offering a brief writeup here because you might come across it
if you look at other projects, and it needs an explanation.

It is used instead of setuptools::

    from rjgtoys.projects import setup

    setup(
        name="...",
        version="...",
        ...
    )

It has some side-effects:

Extended 'test' command
-----------------------

The 'test' command uses `pytest` and `coverage`, so that an HTML coverage
report is generated.

'lint' command
--------------

It adds a 'lint' command that runs `pylint`.

'jenkins' command
-----------------

It adds a 'jenkins' command that will create a Jenkins job to build the project.


