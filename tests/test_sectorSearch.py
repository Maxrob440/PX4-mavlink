import math
import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from sectorSearch import SectorSearch 


def test_initial_state():
    ss = SectorSearch(0.0, 0.0, 10.0)

    assert ss.centreX == 0.0
    assert ss.centreY == 0.0
    assert ss.centreZ == 10.0

    assert ss.currentX == 0.0
    assert ss.currentY == 0.0
    assert ss.currentZ == 10.0

    assert ss.currentAngle == 0
    assert ss.searchRadius == 400
    assert ss.sectorCount == 0
    assert ss.rotationCount == 0

def test_full_three_rotations_nine_steps():
    ss = SectorSearch(0.0, 0.0, 0.0)

    r = 400.0
    sqrt3 = math.sqrt(3)

    expected = [
        (r * 1.0, 0.0, 0.0),                    # step 1: 0°
        (r * 0.5, r * sqrt3 / 2.0, 0.0),        # step 2: 120°
        (0.0, 0.0, 0.0),                        # step 3: centre

        (-r * 0.5, r * sqrt3 / 2.0, 0.0),       # step 4: 120°
        (-r * 1.0, 0.0, 0.0),                   # step 5: 240°
        (0.0, 0.0, 0.0),                        # step 6: centre

        (-r * 0.5, -r * sqrt3 / 2.0, 0.0),      # step 7: 240°
        (r * 0.5, -r * sqrt3 / 2.0, 0.0),       # step 8: 0°
        (0.0, 0.0, 0.0),                        # step 9: centre
    ]

    results = [ss.step() for _ in range(9)]

    for result, exp in zip(results, expected):
        assert result == pytest.approx(exp, abs=0.01)

    # After 3 rotations we should be back at centre
    assert ss.currentX == pytest.approx(0.0, abs=0.01)
    assert ss.currentY == pytest.approx(0.0, abs=0.01)
    assert ss.currentZ == 0.0

    assert ss.rotationCount == 3
    assert ss.sectorCount == 0
    # angle should be back to 0 by the end of third rotation
    assert ss.currentAngle == 0


def test_reset_angle_after_three_rotations():
    ss = SectorSearch(0.0, 0.0, 0.0)

    # Do 3 full rotations (9 steps)
    for _ in range(9):
        ss.step()

    pos = ss.step()

    r = 400.0
    sqrt3 = math.sqrt(3)

    expected = (r * sqrt3 / 2.0, r * 0.5, 0.0)  # (346.41, 200, 0)
    assert pos == pytest.approx(expected, abs=0.01)

    assert ss.rotationCount == 0
    assert ss.currentAngle == 30
    assert ss.sectorCount == 1
