
# See: http://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
import sys

import setuptools

from setuptools.command.test import test as TestCommand


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def readfile(fname):
    return open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), fname)).read()

# See: http://pytest.org/latest/goodpractises.html


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-s'] # preserve stdout
        self.test_suite = True
    def run_tests(self):
        #import here, because outside the eggs aren't loaded
        import pytest
        import coverage
        import time
        import re
        
        wd = os.path.dirname(sys.modules['__main__'].__file__)
        toys = os.path.join(wd,'rjgtoys')
        cov_file = os.path.join(wd,'.coverage')
        if os.path.exists(cov_file):
            os.unlink(cov_file)

        packages = [d for d in os.listdir(toys) if os.path.isdir(os.path.join(toys,d))]
        
        cov = coverage.coverage(include=['rjgtoys/*','tests/unit/fixture*'])
        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.save()

        
        cov_dir = os.path.join(wd,'htmlcov')
        try:
            cov.html_report(directory=cov_dir)
        except coverage.misc.CoverageException as e:
            print("Coverage report error: %s" % (e))
        
        index_html = os.path.join(cov_dir,'index.html')

        if os.path.isfile(index_html):

            # Now fix up the report to have a nice title
            
            cov_title = "Coverage report for %s created at %s" % (",".join(packages),time.strftime("%Y-%m-%d %H:%M:%S"))
            
            report = readfile(index_html)
            report = re.sub('Coverage report',cov_title,report)
            
            with open(index_html,"w") as f:
                f.write(report)
        
        sys.exit(errno)


def setup(**kwargs):
    kwargs.setdefault('tests_require',['pytest'])
    cmdclass = kwargs.get('cmdclass',{})
    cmdclass.setdefault('test',PyTest)

    kwargs['cmdclass'] = cmdclass

    return setuptools.setup(**kwargs)

