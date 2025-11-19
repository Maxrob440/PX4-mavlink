import pytest
from paralellSweep import ParalellSweep


def make_sweep():
    sweep = ParalellSweep(0, 0, 0)

    # Known starting state
    sweep.initialX = 0.0
    sweep.initialY = 0.0
    sweep.initialZ = 0.0

    sweep.currentX = 0.0
    sweep.currentY = 0.0
    sweep.currentZ = 0.0

    sweep.maxX = 100.0     
    sweep.initial = True
    sweep.movedDown = False

    return sweep


def test_first_step_moves_to_right_edge():
    sweep = make_sweep()

    x, y, z = sweep.step()

    assert (x, y, z) == pytest.approx((100.0, 0.0, 0.0), abs=0.01)
    assert sweep.initial is False
    assert sweep.movedDown is False


def test_second_step_moves_down_from_right_edge():
    sweep = make_sweep()
    sweep.step()  

    x, y, z = sweep.step()

    assert (x, y, z) == pytest.approx((100.0, -10.0, 0.0), abs=0.01)
    assert sweep.movedDown is True


def test_third_step_moves_to_left_edge():
    sweep = make_sweep()
    sweep.step() 
    sweep.step()

    x, y, z = sweep.step()

    assert (x, y, z) == pytest.approx((-100.0, -10.0, 0.0), abs=0.01)
    assert sweep.movedDown is False


def test_fourth_step_moves_down_from_left_edge():
    sweep = make_sweep()
    sweep.step()
    sweep.step()
    sweep.step()

    x, y, z = sweep.step()

    assert (x, y, z) == pytest.approx((-100.0, -20.0, 0.0), abs=0.01)
    assert sweep.movedDown is True


def test_fifth_step_moves_back_to_right_edge():
    sweep = make_sweep()
    for _ in range(4):
        sweep.step()

    x, y, z = sweep.step()

    assert (x, y, z) == pytest.approx((100.0, -20.0, 0.0), abs=0.01)
    assert sweep.movedDown is False


def test_z_coordinate_stays_constant():
    sweep = make_sweep()
    initial_z = sweep.currentZ

    for _ in range(10):
        x, y, z = sweep.step()
        assert z == pytest.approx(initial_z, abs=0.01)

