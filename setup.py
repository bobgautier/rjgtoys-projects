#!/usr/bin/python3

from setuptools import setup

from rjgtoys.projects import setup, readfile

setup(
    name = "rjgtoys.projects",
    version = "0.0.1",
    author = "Bob Gautier",
    author_email = "bob@rjg-resources.com",
    description = ("Setuptools extensions to help with rjgtoys projects"),
    long_description = readfile('README'),
    license = "GPL",
    keywords = "setuptools",
    namespace_packages=['rjgtoys'],
    packages = ['rjgtoys.projects'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
        ],
    install_requires = [
	"python-jenkins",
	"GitPython",
        "Jinja2"
    ]
)
