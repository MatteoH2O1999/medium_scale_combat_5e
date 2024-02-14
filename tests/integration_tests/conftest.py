import os
import pytest


@pytest.fixture
def executable_path():
    rootdir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(rootdir, "dist", "main")
