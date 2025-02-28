import math
import os
import pathlib
import random
import sys


from typing import Tuple


import matplotlib.pyplot as plt
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
import sample


@pytest.fixture
def M_Nm() -> float:
    return random.normalvariate(100, 10)


def test_centroid_m(centroid_m:Tuple[float], height_m:Tuple[float]) -> Tuple[float]:
    # is centroid_m[i] is located at the half of the i'th area?
    assert math.isclose(centroid_m[0]*2, height_m[0])
    assert math.isclose((centroid_m[1] - height_m[0])*2, height_m[1])
    assert math.isclose((centroid_m[2] - (height_m[0]+height_m[1]))*2, height_m[2])


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
def result_area(wh:Tuple[float]):
    return exercise.area(*wh)


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
    return exercise.centroid_y(*wh)


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
        expected_centroid_m:float,
        width_m:Tuple[float], height_m:Tuple[float]):
    try:
        assert math.isclose(result_centroid_y, expected_centroid_m, rel_tol=1e-3), (
            '\n'
            f"returned value {result_centroid_y:g} is not close to expected {expected_centroid_m:g}\n"
            f"반환값 {result_centroid_y:g} 이(가) 예상 값 {expected_centroid_m:g} 과 거리가 있음\n"
        )
    except AssertionError as e:
        ax = plt.gca()
        sample.plot_section(ax, result_centroid_y, *width_m, *height_m,)
        ax.axhline(y=expected_centroid_m, color='red', linestyle='-.')
        ax.set_title('result -- expected -.-')
        plt.savefig('check_centroid.png')
        raise e


@pytest.fixture
def result_moment_of_inertia(wh:Tuple[float]):
    return exercise.moment_of_inertia(*wh)


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
    return exercise.bending_stress(M_Nm, *wh)


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
