import itertools
import math
import pathlib
import random
import sys


from typing import Dict, Tuple


import pytest


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))


# Import the functions you'll be testing from your beam_analysis module
import beam_analysis as ba


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
def M_Nm() -> float:
    return random.normalvariate(100, 10)


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
def tot_area_m2(area_m2:Tuple[float]) -> float:
    return sum(area_m2)


@pytest.fixture
def centroid_m(height_m:Tuple[float]) -> Tuple[float]:
    return (
        height_m[0]*0.5,
        height_m[0] + height_m[1]*0.5,
        height_m[0] + height_m[1] + height_m[2]*0.5,
    )


def test_centroid_m(centroid_m:Tuple[float], height_m:Tuple[float]) -> Tuple[float]:
    # is centroid_m[i] is located at the half of the i'th area?
    assert math.isclose(centroid_m[0]*2, height_m[0])
    assert math.isclose((centroid_m[1] - height_m[0])*2, height_m[1])
    assert math.isclose((centroid_m[2] - (height_m[0]+height_m[1]))*2, height_m[2])


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


@pytest.fixture
def I_m4(width_m:float, height_m:float) -> Tuple[float]:
    return tuple(
        map(
            lambda x_y: x_y[0] * (x_y[1]**3) / 12.0,
            zip(
                width_m, height_m
            )
        )
    )


@pytest.fixture
def tot_I_m4(
        I_m4:Tuple[float],
        area_m2:Tuple[float],
        centroid_m:Tuple[float],
        expected_centroid_m:float,
    ) -> float:
    return sum(
        map(
            lambda i_a_y: (
                i_a_y[0] + i_a_y[1] * (
                    expected_centroid_m - i_a_y[2]
                )**2
            ),
            zip(
                I_m4, area_m2, centroid_m
            )
        )
    )


@pytest.fixture
def wh(width_m:Tuple[float], height_m:Tuple[float]) -> Tuple[float]:
    return tuple(
        itertools.chain.from_iterable(
            zip(width_m, height_m)
        )
    )


@pytest.fixture
def result_area(wh:Tuple[float]):
    return ba.area(*wh)


@pytest.mark.area
def test_result_area_float(result_area:float):
    assert isinstance(result_area, float), (
        '\n'
        f"returned value is not a float : {result_area} {type(result_area)}\n"
        f"반환값이 float가 아님 : {result_area} {type(result_area)}\n"
    )


@pytest.mark.area
def test_result_area_value(result_area:float, tot_area_m2:float):
    assert math.isclose(result_area, tot_area_m2, rel_tol=1e-3), (
        '\n'
        f"returned value {result_area:g} is not close to expected {tot_area_m2:g}\n"
        f"반환값 {result_area:g} 이(가) 예상 값 {tot_area_m2:g} 과 거리가 있음\n"
    )


@pytest.fixture
def result_centroid_y(wh:Tuple[float]):
    return ba.centroid_y(*wh)


@pytest.mark.centroid_y
def test_result_centroid_y_float(result_centroid_y:float):
    assert isinstance(result_centroid_y, float), (
        '\n'
        f"returned value is not a float : {result_centroid_y} {type(result_centroid_y)}\n"
        f"반환값이 float가 아님 : {result_centroid_y} {type(result_centroid_y)}\n"
    )


@pytest.mark.centroid_y
def test_result_centroid_y_value(
        result_centroid_y:float,
        expected_centroid_m:float):
    assert math.isclose(result_centroid_y, expected_centroid_m, rel_tol=1e-3), (
        '\n'
        f"returned value {result_centroid_y:g} is not close to expected {expected_centroid_m:g}\n"
        f"반환값 {result_centroid_y:g} 이(가) 예상 값 {expected_centroid_m:g} 과 거리가 있음\n"
    )


@pytest.fixture
def result_area_above_below_equal(wh:Tuple[float]):
    return ba.area_above_below_equal(*wh)


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
    return ba.area_moment_above_below_equal(*wh)


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


@pytest.fixture
def result_moment_of_inertia(wh:Tuple[float]):
    return ba.moment_of_inertia(*wh)


@pytest.mark.moment_of_inertia
def test_result_moment_of_inertia_float(result_moment_of_inertia:float):
    assert isinstance(result_moment_of_inertia, float), (
        '\n'
        f"returned value is not a float : {result_moment_of_inertia} {type(result_moment_of_inertia)}\n"
        f"반환값이 float가 아님 : {result_moment_of_inertia} {type(result_moment_of_inertia)}\n"
    )


@pytest.mark.moment_of_inertia
def test_result_moment_of_inertia_value(result_moment_of_inertia:float, tot_I_m4:float):
    assert math.isclose(result_moment_of_inertia, tot_I_m4, rel_tol=1e-3), (
        '\n'
        f"returned value {result_moment_of_inertia:g} is not close to expected {tot_I_m4:g}\n"
        f"반환값 {result_moment_of_inertia:g} 이(가) 예상 값 {tot_I_m4:g} 과 거리가 있음\n"
    )


@pytest.fixture
def result_bending_stress(M_Nm:float, wh:Tuple[float]):
    return ba.bending_stress(M_Nm, *wh)


@pytest.fixture
def expected_bending_stress_Pa(M_Nm:float, height_m:Tuple[float], tot_I_m4:float, expected_centroid_m:float):
    return max(abs(M_Nm * expected_centroid_m / tot_I_m4), abs(M_Nm * (sum(height_m) - expected_centroid_m) / tot_I_m4))


@pytest.mark.bending_stress
def test_bending_stress_type(result_bending_stress:float):
    assert isinstance(result_bending_stress, float), (
        '\n'
        f"returned value is not a float : {result_bending_stress} {type(result_bending_stress)}\n"
        f"반환값이 float가 아님 : {result_bending_stress} {type(result_bending_stress)}\n"
    )


@pytest.mark.bending_stress
def test_result_result_bending_stress_value(
        result_bending_stress:float,
        expected_bending_stress_Pa:float):
    assert math.isclose(result_bending_stress, expected_bending_stress_Pa, rel_tol=1e-3), (
        '\n'
        f"returned value {result_bending_stress:g} is not close to expected {expected_bending_stress_Pa:g}\n"
        f"반환값 {result_bending_stress:g} 이(가) 예상 값 {expected_bending_stress_Pa:g} 과 거리가 있음\n"
    )


if "__main__" == __name__:
    pytest.main([__file__])
