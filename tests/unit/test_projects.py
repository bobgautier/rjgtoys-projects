
from rjgtoys.projects import readfile

def test_readfile():
    content = readfile("tests/unit/readfile_testdata")
    assert content == "This is test data for test_readfile.\n"

