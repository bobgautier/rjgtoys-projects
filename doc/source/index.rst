rjgtoys.projects: A simple wrapper for setuptools
=================================================

Provides an alternative to the :func:`setuptools.setup` function
that defines a Python project.

This package is very specific to how I like to build projects, and
I doubt it will be of much use to anyone else.

I'm offering a brief writeup here because you might come across it
if you look at my other projects, so it needs an explanation.

In order to be able to build other `rjgtoys` projects you'll need to get
past the first two steps at least.

Getting it
==========

This package is not (yet) on PyPi.   To get the source code::

    git clone https://github.com/bobgautier/rjgtoys-projects.git

Making it usable
================

To make the package available for your Python::

    cd rjgtoys-projects
    python ./setup.py develop --user

If you are using a virtualenv, you should omit the ``--user`` option used
in these examples.

Once you've done this, the `setup.py` from other `rjgtoys` projects should work
more or less as you expect.


.. include:: cli.rst



Using `setup.py`
================

My version of :func:`setup()` adds some new commands, and customises
some existing ones.

Extended 'test' command
-----------------------

The 'test' command uses `pytest` and `coverage`, so that an HTML coverage
report is generated.

You will find the coverage report at ``htmlcov/index.html`` in your project tree.

The command goes to some trouble to enumerate all the Python source code files
in your project tree, so that they are included in the coverage report even if
they are not referenced by any tests.   This is to avoid making coverage look
good when only a few modules have any tests at all.

Using `setuptools` to run tests is now deprecated, so eventually I will have
to find a different way to do this.

'lint' command
--------------

The 'lint' command runs `pylint`.

The configuration is embedded in `rjgtoys-projects` (so that it's standard for
all my projects).

The report is left in the project directory, in ``pylint.out``.

'jenkins' command
-----------------

The 'jenkins' command can create a Jenkins job to build the project.

This command is just an old experimental proof-of-concept.

Credits
=======

The templating is all done with Cookiecutter_.

.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/1.7.2/

