from src.rectangle import Rectangle
from src.square import Square
from src.circle import Circle
import pytest


@pytest.mark.parametrize(
    ("side_a", "area", "perimeter"),
    [
        pytest.param(7, 49, 28, marks=[pytest.mark.positive], id='integer'),
        pytest.param(10.35, 107.12, 41.4, marks=[pytest.mark.positive], id='float')
    ]
)
def test_square_sides(side_a, area, perimeter):
    s = Square(side_a)
    assert s.area == area, f"The Area result was just calculated does not corresponds according to side values: side_a = {r.side_a}"
    assert s.perimeter == perimeter, f"The Perimeter result was just calculated does not corresponds according to side values: side_a = {r.side_a}"


@pytest.mark.parametrize(
    ("side_a"),
    [
        pytest.param(0, marks=[pytest.mark.negative], id='zero'),
        pytest.param(-123, marks=[pytest.mark.negative], id='below zero')
    ]
)
def test_rectangle_int(side_a):
    with pytest.raises(ValueError, match="Side parameter value must be above zero"):
        Square(side_a)


@pytest.mark.parametrize(
    ("side_a"),
    [
        pytest.param('65', marks=[pytest.mark.negative], id='int in quotes'),
        pytest.param('this_is_string', marks=[pytest.mark.negative], id='letter in quotes')
    ]
)
def test_rectangle_string(side_a):
    with pytest.raises(TypeError, match='Side parameters must be type: "int" or "float"'):
        Square(side_a)


@pytest.mark.parametrize(
    ("side_a_rectangle", "side_b_rectangle", "side_square", "radius_circle", "sum_area_sq_rec", "sum_area_sq_cir"),
    [
        pytest.param(8, 11, 5, 7, 113, 178.94, marks=[pytest.mark.positive], id='add area, integer'),
        pytest.param(10.2, 8.3, 4.1, 8.9, 101.47, 265.66, marks=[pytest.mark.positive], id='add area, float')
    ]
)
def test_rectangle_add_areas(side_a_rectangle, side_b_rectangle, side_square, radius_circle, sum_area_sq_rec, sum_area_sq_cir):
    test_rectangle = Rectangle(side_a_rectangle, side_b_rectangle)
    test_circle = Circle(radius_circle)
    test_square = Square(side_square)
    assert test_square.add_area(test_rectangle) == sum_area_sq_rec, "The sum area of test_rectangle_1 and test_rectangle_2 does not correspond to calculations"
    assert test_square.add_area(test_circle) == sum_area_sq_cir, "The sum area of test_rectangle_1 and test_square does not correspond to calculations"
