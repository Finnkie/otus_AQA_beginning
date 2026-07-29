from src.rectangle import Rectangle
from src.square import Square
import pytest


@pytest.mark.parametrize(
    ("side_a", "side_b", "area", "perimeter"),
    [
        pytest.param(10, 7, 70, 34, marks=[pytest.mark.positive], id="integer"),
        pytest.param(5.5, 10.35, 56.92, 31.7, marks=[pytest.mark.positive], id="float"),
    ],
)
def test_rectangle_sides(side_a, side_b, area, perimeter):
    r = Rectangle(side_a, side_b)
    assert r.area == area, (
        f"The Area result was just calculated does not corresponds according to side values: side_a = {r.side_a} and side_b = {r.side_b}"
    )
    assert r.perimeter == perimeter, (
        f"The Perimeter result was just calculated does not corresponds according to side values: side_a = {r.side_a} and side_b = {r.side_b}"
    )


@pytest.mark.parametrize(
    ("side_a", "side_b"),
    [
        pytest.param(3.3, 0, marks=[pytest.mark.negative], id="zero"),
        pytest.param(-3, 5, marks=[pytest.mark.negative], id="below zero"),
    ],
)
def test_rectangle_int(side_a, side_b):
    with pytest.raises(ValueError, match="Side parameters must be above zero"):
        Rectangle(side_a, side_b)
