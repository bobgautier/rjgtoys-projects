#!/usr/bin/python3

# Bootstrap support: If this package can't (yet) be imported,
# fall back to regular setuptools.
#
# This makes an initial 'setup.py develop --user' work.
#

try:
    from rjgtoys.projects import setup
except ImportError:
    from setuptools import setup

setup(
    name = "rjgtoys-projects",
    version = "0.0.1",
    author = "Robert J Gautier",
    author_email = "bob.gautier@gmail.com",
    description = ("Setuptools extensions to help with rjgtoys projects"),
    keywords = "setuptools",
    namespace_packages=['rjgtoys'],
    packages = ['rjgtoys.projects'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    install_requires = [
        "python-jenkins",
        "GitPython",
        "Jinja2"
    ],
    python_requires='>=3.6'
)
