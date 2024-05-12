import pathlib

from typing import Tuple


import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = test_folder.parent.absolute()



def py_files() -> Tuple[pathlib.Path]:
    return tuple(
        filter(
            lambda s:'sample.py' != s.name,
            proj_folder.glob('*.py')
        )
    )


def pytest_generate_tests(metafunc):
    if "py_file" in metafunc.fixturenames:
        metafunc.parametrize("py_file", py_files())


def pytest_configure(config):
    config.addinivalue_line("markers", "area: tests for area calculations")
    config.addinivalue_line("markers", "centroid_y: tests for centroid_y calculations")
    config.addinivalue_line("markers", "area_above_below_equal: tests for area_above_below_equal function")
    config.addinivalue_line("markers", "area_moment_above_below_equal: tests for area_moment_above_below_equal function")
    config.addinivalue_line("markers", "moment_of_inertia: tests for moment of inertia calculations")
    config.addinivalue_line("markers", "bending_stress: tests for bending stress calculations")
