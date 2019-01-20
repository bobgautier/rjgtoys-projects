"""
Extended setup() function.
"""

import setuptools

from rjgtoys.projects._test import PyTest
from rjgtoys.projects._lint import LintCommand
from rjgtoys.projects._jenkins import JenkinsCommand

def setup(**kwargs):
    """Replacement for `setuptools.setup()`."""

    kwargs.setdefault('tests_require', ['pytest', 'coverage'])
    cmdclass = kwargs.get('cmdclass', {})
    cmdclass.setdefault('test', PyTest)
    cmdclass.setdefault('lint', LintCommand)
    cmdclass.setdefault('jenkins', JenkinsCommand)

    kwargs['cmdclass'] = cmdclass

    return setuptools.setup(**kwargs)
