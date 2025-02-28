import os
import math
import pathlib
import sys

from typing import Dict, Tuple


import pytest

sys.path.insert(
    0,
    os.getenv(
        'STUDENT_CODE_FOLDER',
        str(
            pathlib.Path(__file__).parent.parent.absolute()
        )
    )
)


# Import the functions you'll be testing from your beam_analysis module
import exercise


@pytest.fixture
def result_area_above_below_equal(wh:Tuple[float]):
    return exercise.area_above_below_equal(*wh)


@pytest.fixture
def expected_a_above_below(
    expected_centroid_m:float,
    area_m2:Tuple[float],
    width_m:Tuple[float],
    height_m:Tuple[float],) -> Dict[str, float]:
    h1_below_m = expected_centroid_m - height_m[0]
    area_below_m2 = area_m2[0] + h1_below_m * width_m[1]
    h1_above_m = height_m[0] + height_m[1] - expected_centroid_m
    area_above_m2 = area_m2[2] + h1_above_m * width_m[1]

    return {
        'a_above': area_above_m2,
        'a_below': area_below_m2,
        'close': math.isclose(area_above_m2, area_below_m2)
    }


@pytest.mark.area_above_below_equal
def test_result_area_above_below_type(result_area_above_below_equal:float):
    assert isinstance(result_area_above_below_equal, dict), (
        '\n'
        "returned value is not a dict : "
        f"{result_area_above_below_equal} "
        f"{type(result_area_above_below_equal)}\n"
        "반환값이 dict 가 아님 : "
        f"{result_area_above_below_equal} "
        f"{type(result_area_above_below_equal)}\n"
    )


@pytest.mark.area_above_below_equal
def test_result_area_above_below_keys(
        result_area_above_below_equal:Dict[str, float],
        expected_a_above_below:Dict[str, float]):

    returned_keys = list(set(result_area_above_below_equal.keys()))
    returned_keys.sort()

    expecteded_keys = list(set(expected_a_above_below.keys()))
    expecteded_keys.sort()

    assert returned_keys == expecteded_keys, (
        '\n'
        f"returned keys {returned_keys} different from expected {expecteded_keys}.\n"
        f"반환값의 key {returned_keys} 이(가) 예상과 다름 {expecteded_keys}.\n"
    )


@pytest.mark.area_above_below_equal
def test_result_area_above_below_value_above(
        result_area_above_below_equal:Dict[str, float],
        expected_a_above_below:Dict[str, float]):

    result_a_above = result_area_above_below_equal['a_above']
    expected_a_above = expected_a_above_below['a_above']

    assert math.isclose(result_a_above, expected_a_above, rel_tol=1e-3), (
        '\n'
        f"returned value {result_a_above:g} is not close to expected {expected_a_above:g}\n"
        f"반환값 {result_a_above:g} 이(가) 예상 값 {expected_a_above:g} 과 거리가 있음\n"
    )


@pytest.mark.area_above_below_equal
def test_result_area_above_below_value_below(
        result_area_above_below_equal:Dict[str, float],
        expected_a_above_below:Dict[str, float]):

    result_a_below = result_area_above_below_equal['a_below']
    expected_a_below = expected_a_above_below['a_below']

    assert math.isclose(result_a_below, expected_a_below, rel_tol=1e-3), (
        '\n'
        f"returned value {result_a_below:g} is not close to expected {expected_a_below:g}\n"
        f"반환값 {result_a_below:g} 이(가) 예상 값 {expected_a_below:g} 과 거리가 있음\n"
    )


@pytest.mark.area_above_below_equal
def test_result_area_above_below_value_close(
        result_area_above_below_equal:Dict[str, float],
        expected_a_above_below:Dict[str, float]):

    result_close = result_area_above_below_equal['close']
    expected_close = expected_a_above_below['close']

    assert result_close == expected_close, (
        '\n'
        f"returned value {expected_close} is not equal to expected {expected_close:g}\n"
        f"반환값 {expected_close} 이(가) 예상 값 {expected_close:g} 과 같지 않음\n"
    )


@pytest.fixture
def result_area_moment_above_below_equal(wh:Tuple[float]):
    return exercise.area_moment_above_below_equal(*wh)


@pytest.fixture
def expected_a_moment_above_below(
    expected_centroid_m:float,
    area_m2:Tuple[float],
    width_m:Tuple[float],
    centroid_m:Tuple[float],
    height_m:Tuple[float],) -> Dict[str, float]:

    h1_below_m = expected_centroid_m - height_m[0]
    area_moment_below_m3 = (
          area_m2[0]*(expected_centroid_m - centroid_m[0])
        + h1_below_m * width_m[1] * (0.5) * h1_below_m)

    h1_above_m = height_m[0] + height_m[1] - expected_centroid_m
    area_moment_above_m3 = (
          area_m2[2]*(centroid_m[2] - expected_centroid_m)
        + h1_above_m * width_m[1] * (0.5) * h1_above_m)

    return {
        'a_moment_above': area_moment_below_m3,
        'a_moment_below': area_moment_above_m3,
        'close': math.isclose(area_moment_below_m3, area_moment_above_m3)
    }


def test_expected_centroid(
        expected_a_moment_above_below:Dict[str, float],
    ):
    assert math.isclose(
        expected_a_moment_above_below['a_moment_above'],
        expected_a_moment_above_below['a_moment_below']
    )


@pytest.mark.area_moment_above_below_equal
def test_result_area_moment_above_below_equal_type(
        result_area_moment_above_below_equal:float):
    assert isinstance(result_area_moment_above_below_equal, dict), (
        '\n'
        f"returned value is not a dict : {result_area_moment_above_below_equal} "
        f"{type(result_area_moment_above_below_equal)}\n"
        f"반환값이 dict 가 아님 : {result_area_moment_above_below_equal} "
        f"{type(result_area_moment_above_below_equal)}\n"
    )


@pytest.mark.area_moment_above_below_equal
def test_result_area_moment_above_below_equal_keys(
        result_area_moment_above_below_equal:Dict[str, float],
        expected_a_moment_above_below:Dict[str, float]):

    returned_keys = list(set(result_area_moment_above_below_equal.keys()))
    returned_keys.sort()

    expecteded_keys = list(set(expected_a_moment_above_below.keys()))
    expecteded_keys.sort()

    assert returned_keys == expecteded_keys, (
        '\n'
        f"returned keys {returned_keys} different from expected {expecteded_keys}.\n"
        f"반환값의 key {returned_keys} 이(가) 예상과 다름 {expecteded_keys}.\n"
    )


@pytest.mark.area_moment_above_below_equal
def test_result_area_moment_above_below_equal_value_above(
        result_area_moment_above_below_equal:Dict[str, float],
        expected_a_moment_above_below:Dict[str, float]):

    result_a_above = result_area_moment_above_below_equal['a_moment_above']
    expected_a_above = expected_a_moment_above_below['a_moment_above']

    assert math.isclose(result_a_above, expected_a_above, rel_tol=1e-3), (
        '\n'
        f"returned value {result_a_above:g} is not close to expected {expected_a_above:g}\n"
        f"반환값 {result_a_above:g} 이(가) 예상 값 {expected_a_above:g} 과 거리가 있음\n"
    )


@pytest.mark.area_moment_above_below_equal
def test_result_area_moment_above_below_equal_value_below(
        result_area_moment_above_below_equal:Dict[str, float],
        expected_a_moment_above_below:Dict[str, float]):

    result_a_below = result_area_moment_above_below_equal['a_moment_below']
    expected_a_below = expected_a_moment_above_below['a_moment_below']

    assert math.isclose(result_a_below, expected_a_below, rel_tol=1e-3), (
        '\n'
        f"returned value {result_a_below:g} is not close to expected {expected_a_below:g}\n"
        f"반환값 {result_a_below:g} 이(가) 예상 값 {expected_a_below:g} 과 거리가 있음\n"
    )


@pytest.mark.area_moment_above_below_equal
def test_result_area_moment_above_below_equal_value_close(
        result_area_moment_above_below_equal:Dict[str, float],
        expected_a_moment_above_below:Dict[str, float]):

    result_close = result_area_moment_above_below_equal['close']
    expected_close = expected_a_moment_above_below['close']

    assert result_close == expected_close, (
        '\n'
        f"returned value {expected_close} is not equal to expected {expected_close:g}\n"
        f"반환값 {expected_close}  예상 값 {expected_close:g} 과 같지 않음\n"
    )


if "__main__" == __name__:
    pytest.main([__file__])
