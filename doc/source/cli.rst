Starting a new project: `rjgtoys-new`
=====================================

This command line tool simplifies starting a new project; it creates
an empty project tree based on a few parameters you provide either
in a configuration file or on the command line.

Command line options
--------------------

Use ``--help`` to get a list of options::

    $ rjgtoys-new --help
    usage: Build a new rjgtoys project [-h] [--name NAME] [--id IDENT] --title TEXT [--template PATH] [--update] [--config PATH] [--dry-run]

    optional arguments:
      -h, --help       show this help message and exit
      --name NAME      Public name of the project, for docs etc.
      --id IDENT       Internal name of the project, for directories etc.
      --title TEXT     One-line title for the project
      --template PATH  Template name or path (default: rjgtoys)
      --update         Update an existing project (default: False)
      --config PATH    Configuration to use (default: $HOME/.config/rjgtoys/projects/projects.conf)
      --dry-run, -n    Don't generate anything, just validate (default: False)

--id
  A short name for the project, used for directories, files, and so on.
  This name will be used for the main package source directory of the project.

--name
  A 'documentation name' for the project; usually very similar or identical to the
  `id`, but sometimes capitalised, or slightly modified in some other way.

  For example, `rjgtoys-xc` (id: `xc`) has the `name` `XC` because I think that
  looks better in documentation.

--title
  A one-line description of the project.

--template
  The name of a template set to use for the project.   This is a path,
  and relative paths are interpreted relative to a ``templates`` directory
  internal to `rjgtoys-projects`.

  If you want to experiment with this, be prepared to learn about Cookiecutter_.

--update
  If this option is used, ``rjgtoys-new`` will update an existing directory
  (and might therefore lose you some work).

--config
  Specifies a configuration file from which to get further parameters for the
  project.   The configuration file is described below.

--dry-run
  If used, no files or directories will be created or updated.


The project tree is created (or updated) in a directory named with the `id` you
specified.

Configuration file
------------------

.. literalinclude:: ../../examples/projects.conf

The file is YAML.

The parameters are as follows.   For brevity I've used dotted names here,
to indicate the paths through the nested mappings that are expected in the
configuration file.

project.family
  Name of the group to which the project belongs.  The default is `rjgtoys`,
  resulting in projects called ``rjgtoys-ID``.

  If you start using this tool yourself, please use a different family name;
  I chose `rjgtoys` in the hope of avoiding a clash with someone else.

copyright.year
  The year to include in copyright notices.

author.fullname
  Full name of the author.

author.email
  Email address of author.

github.base
  Base URL for github repos; project repositories will be expected to be
  'under' this URL.


