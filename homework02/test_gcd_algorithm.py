import pytest
import math
from gcd_algorithm import greatCircleDistance

def test_greatCircleDistance():
    assert greatCircleDistance(0,0,0,0) == 0
    assert math.isclose(greatCircleDistance(0,0,90,0), 10000, abs_tol=20)
