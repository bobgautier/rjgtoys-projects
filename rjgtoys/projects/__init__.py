"""
Customisations for setuptools, to support test coverage
reports and style scoring using pylint.

"""

# See: http://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
import sys
import subprocess
import contextlib
import operator
import itertools

from distutils.errors import DistutilsOptionError

import setuptools
from setuptools.command.test import test as TestCommand

# pylint: disable=no-name-in-module
from setuptools.extern import six

from pkg_resources import (resource_listdir, resource_exists, normalize_path,
                           working_set, _namespace_packages, evaluate_marker,
                           add_activation_listener, require, EntryPoint)


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
        ('lint-report=', None, "Where to write the lint report (default: ./pylint.out)"),
        ('lint-requires', None, "List of modules needed to run pylint (default: pylint)")
 ]

    def initialize_options(self):
        """Set initial values for the command options."""
        self.lint_rc = os.path.join(os.path.dirname(__file__), 'pylintrc')
        self.lint_report = "pylint.out"
        self.lint_requires = "pylint"

    def finalize_options(self):
        """Set final values for the command options."""
        if not os.path.isfile(self.lint_rc):
            raise DistutilsOptionError("pylintrc file '%s' does not exist" % (self.lint_rc))

    def run(self):
        """Run pylint."""

        # All this fuss with paths_on... is copied from the test command

        deps = self.install_dists(self.distribution, self.lint_requires.split(","))

        paths = map(operator.attrgetter('location'), deps)
        with self.paths_on_pythonpath(paths):
            with self.project_on_sys_path():
                self.run_lint()

    def run_lint(self):
        """Run pylint and capture the report."""

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

    # The following is copied from setuptools.command.test
    # because it appears to be needed to get dependencies
    # working.

    @staticmethod
    def install_dists(dist, lint_requires):
        """
        Install the requirements indicated by self.distribution and
        return an iterable of the dists that were built.
        """
        ir_d = dist.fetch_build_eggs(lint_requires)
        tr_d = dist.fetch_build_eggs(dist.tests_require or [])
        er_d = dist.fetch_build_eggs(
            v for k, v in dist.extras_require.items()
            if k.startswith(':') and evaluate_marker(k[1:])
        )
        return itertools.chain(ir_d, tr_d, er_d)

    @contextlib.contextmanager
    def project_on_sys_path(self, include_dists=None):
        """Put this project on `sys.path`."""

        # pylint: disable=unused-argument
        include_dists = include_dists or []
        with_2to3 = six.PY3 and getattr(self.distribution, 'use_2to3', False)

        if with_2to3:
            # If we run 2to3 we cannot do this inplace:

            # Ensure metadata is up-to-date
            self.reinitialize_command('build_py', inplace=0)
            self.run_command('build_py')
            bpy_cmd = self.get_finalized_command("build_py")
            build_path = normalize_path(bpy_cmd.build_lib)

            # Build extensions
            self.reinitialize_command('egg_info', egg_base=build_path)
            self.run_command('egg_info')

            self.reinitialize_command('build_ext', inplace=0)
            self.run_command('build_ext')
        else:
            # Without 2to3 inplace works fine:
            self.run_command('egg_info')

            # Build extensions in-place
            self.reinitialize_command('build_ext', inplace=1)
            self.run_command('build_ext')

        ei_cmd = self.get_finalized_command("egg_info")

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        try:
            project_path = normalize_path(ei_cmd.egg_base)
            sys.path.insert(0, project_path)
            working_set.__init__()
            add_activation_listener(lambda dist: dist.activate())
            require('%s==%s' % (ei_cmd.egg_name, ei_cmd.egg_version))
            with self.paths_on_pythonpath([project_path]):
                yield
        finally:
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)
            working_set.__init__()

    @staticmethod
    @contextlib.contextmanager
    def paths_on_pythonpath(paths):
        """
        Add the indicated paths to the head of the PYTHONPATH environment
        variable so that subprocesses will also see the packages at
        these paths.

        Do this in a context that restores the value on exit.
        """
        nothing = object()
        orig_pythonpath = os.environ.get('PYTHONPATH', nothing)
        current_pythonpath = os.environ.get('PYTHONPATH', '')
        try:
            prefix = os.pathsep.join(paths)
            to_join = filter(None, [prefix, current_pythonpath])
            new_path = os.pathsep.join(to_join)
            if new_path:
                os.environ['PYTHONPATH'] = new_path
            yield
        finally:
            if orig_pythonpath is nothing:
                os.environ.pop('PYTHONPATH', None)
            else:
                os.environ['PYTHONPATH'] = orig_pythonpath


def setup(**kwargs):
    """Replacement for `setuptools.setup()`."""

    kwargs.setdefault('tests_require', ['pytest'])
    kwargs.setdefault('lint_requires', ['pylint'])
    cmdclass = kwargs.get('cmdclass', {})
    cmdclass.setdefault('test', PyTest)
    cmdclass.setdefault('lint', LintCommand)

    kwargs['cmdclass'] = cmdclass

    return setuptools.setup(**kwargs)
