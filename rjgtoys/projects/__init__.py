"""
Customisations for setuptools, to support test coverage
reports and style scoring using pylint.

"""

# See: http://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
import sys
import subprocess

from distutils.errors import DistutilsOptionError

import setuptools
from setuptools.command.test import test as TestCommand


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def readfile(fname):
    """Read a file and return its content."""
    return open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), fname)).read()

# See: http://pytest.org/latest/goodpractises.html


class PyTest(TestCommand):
    """An extended test command that produces coverage reports of tests."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-s'] # preserve stdout
        self.test_suite = True

    def run_tests(self):
        # pylint: disable=too-many-locals
        #import here, because outside the eggs aren't loaded
        import pytest
        import coverage
        import time
        import re

        # Note that here, __main__ refers to the calling project's
        # "setup.py"

        project_root = os.path.dirname(sys.modules['__main__'].__file__)
        cov_file = os.path.join(project_root, '.coverage')
        if os.path.exists(cov_file):
            os.unlink(cov_file)

        packages = setuptools.find_packages(where=project_root)

        include = [os.path.join(p, '*') for p in packages]
        include.append('tests/unit/fixture*')

        cov = coverage.coverage(include=include)

        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.save()

        cov_dir = os.path.join(project_root, 'htmlcov')
        try:
            cov.html_report(directory=cov_dir)
        except coverage.misc.CoverageException as e:
            print("Coverage report error: %s" % (e))

        index_html = os.path.join(cov_dir, 'index.html')

        if os.path.isfile(index_html):

            # Now fix up the report to have a nice title

            cov_title = "Coverage report for %s created at %s" % (
                            ",".join(packages),
                            time.strftime("%Y-%m-%d %H:%M:%S")
                        )

            report = readfile(index_html)
            report = re.sub('Coverage report', cov_title, report)

            with open(index_html, "w") as f:
                f.write(report)

        sys.exit(errno)


class LintCommand(setuptools.Command):
    """Run pylint and produce a report."""

    description = "Perform style checks"

    user_options = [
        ('lint-rc=', None, "Path to the pylintrc file to use (default: built-in)"),
        ('lint-report=', None, "Where to write the lint report (default: ./pylint.out)")
 ]

    def initialize_options(self):
        """Set initial values for the command options."""
        self.lint_rc = os.path.join(os.path.dirname(__file__), 'pylintrc')
        self.lint_report = "pylint.out"

    def finalize_options(self):
        """Set final values for the command options."""
        if not os.path.isfile(self.lint_rc):
            raise DistutilsOptionError("pylintrc file '%s' does not exist" % (self.lint_rc))

    def run(self):
        """Run pylint."""

        with open(self.lint_report, "w") as report:
#            print("Lint configuration from '%s'" % (self.lint_rc))
            print("Lint: Report will be in '%s'" % (self.lint_report))

            cmd = [sys.executable, "-m", "pylint", "--rcfile=%s" % (self.lint_rc), "rjgtoys"]

            p = subprocess.Popen(
                    cmd,
                    stdout=report
            )
            s = p.wait()
            if s == 0:
                print("Lint: PASS")
            if s & 1:
                print("Lint: Fatal error(s)")
            if s & 2:
                print("Lint: Error(s) were found")
            if s & 4:
                print("Lint: Warning(s) were found")
            if s & 8:
                print("Lint: Refactoring suggested")
            if s & 16:
                print("Lint: Style error(s) were found")
            if s & 32:
                print("Lint: Configuration (pylintrc) error")
            self._print_score()

    def _print_score(self):
        """Report the lint score."""

        report = None
        try:
            with open(self.lint_report, 'r') as f:
                for line in f:
                    if line.startswith('Your code has been rated'):
                        report = line.strip()
        except IOError as e:
            report = "Could not determine code score: %s" % (e)

        print("Lint: %s" % (report))


def setup(**kwargs):
    """Replacement for `setuptools.setup()`."""

    kwargs.setdefault('tests_require', ['pytest'])
    cmdclass = kwargs.get('cmdclass', {})
    cmdclass.setdefault('test', PyTest)
    cmdclass.setdefault('lint', LintCommand)

    kwargs['cmdclass'] = cmdclass

    return setuptools.setup(**kwargs)
