"""

Custom 'test' command.

"""

import sys
import os

# See: http://pytest.org/latest/goodpractises.html

import setuptools
from setuptools.command.test import test as TestCommand


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def readfile(fname):
    """Read a file and return its content."""
    return open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), fname)).read()


class PyTest(TestCommand):
    """An extended test command that produces coverage reports of tests."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-s', 'tests'] # preserve stdout
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
