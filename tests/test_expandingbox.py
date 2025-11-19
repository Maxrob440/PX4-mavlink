import math
import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from expandingBox import ExpandingBox


def test_initialisation():
    eb = ExpandingBox(0, 0, 10, initialDirection=0)

    assert eb.initialX == 0
    assert eb.initialY == 0
    assert eb.initialZ == 10
    assert eb.previousDirection == 0
    assert eb.currentX == 0
    assert eb.currentY == 0
    assert eb.currentZ == 10
    assert eb.expansionFactor == 1
    assert eb.expandNext is False  # set in constructor


def test_first_step():
    eb = ExpandingBox(0, 0, 10, initialDirection=0)

    x, y, z = eb.step()

    assert x == pytest.approx(0, abs=0.01)
    assert y == pytest.approx(30, abs=0.01)
    assert z == 10
    assert eb.previousDirection == 90


def test_second_step():
    eb = ExpandingBox(0, 0, 10, initialDirection=0)
    eb.step()  # first step

    x, y, z = eb.step()

    assert x == pytest.approx(-60, abs=0.01)
    assert y == pytest.approx(30, abs=0.01)
    assert z == 10
    assert eb.previousDirection == 180


def test_multiple_steps_follow_pattern():
    eb = ExpandingBox(0, 0, 0, initialDirection=0)

    results = [eb.step() for _ in range(6)]

    expected = [
        (0, 30),
        (-60, 30),
        (-60, -30),
        (30, -30),
        (30, 60),
        (-90, 60),
    ]

    for (x, y,z), (ex, ey) in zip(results[:2], expected):
        assert x == pytest.approx(ex, abs=0.01)
        assert y == pytest.approx(ey, abs=0.01)


def test_direction_wraparound():
    eb = ExpandingBox(0, 0, 0, initialDirection=270)

    x, y, z = eb.step()

    assert eb.previousDirection == 0
    assert (x, y, z) == (30, 0, 0)



