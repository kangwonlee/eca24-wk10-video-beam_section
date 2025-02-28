import itertools
import os
import pathlib
import random

from typing import Tuple

import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()

proj_folder = pathlib.Path(
    os.getenv(
        'STUDENT_CODE_FOLDER',
        test_folder.parent.absolute()
    )
)



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


@pytest.fixture
def width_m() -> Tuple[float]:
    return (
        random.normalvariate(50e-3, 10e-3),
        random.normalvariate(7.5e-3, 1.5e-3),
        random.normalvariate(90e-3, 18e-3)
    )


@pytest.fixture
def height_m() -> Tuple[float]:
    return (
        random.normalvariate(12e-3, 2.5e-3),
        random.normalvariate(70e-3, 1.4e-3),
        random.normalvariate(10e-3, 2e-3)
    )


@pytest.fixture
def wh(width_m:Tuple[float], height_m:Tuple[float]) -> Tuple[float]:
    return tuple(
        itertools.chain.from_iterable(
            zip(width_m, height_m)
        )
    )


@pytest.fixture
def expected_centroid_m(
        area_m2:Tuple[float], centroid_m:Tuple[float],
        tot_area_m2:float,
        ) -> float:
    return sum(
        map(
            lambda a_y: a_y[0] * a_y[1],
            zip(area_m2, centroid_m)
        )
    ) / tot_area_m2


@pytest.fixture
def area_m2(width_m:float, height_m:float) -> Tuple[float]:
    return tuple(
        map(
            lambda x_y: x_y[0] * x_y[1],
            zip(
                width_m, height_m
            )
        )
    )


@pytest.fixture
def centroid_m(height_m:Tuple[float]) -> Tuple[float]:
    return (
        height_m[0]*0.5,
        height_m[0] + height_m[1]*0.5,
        height_m[0] + height_m[1] + height_m[2]*0.5,
    )


@pytest.fixture
def tot_area_m2(area_m2:Tuple[float]) -> float:
    return sum(area_m2)
