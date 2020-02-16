#!/usr/bin/python3

from rjgtoys.projects import setup

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
