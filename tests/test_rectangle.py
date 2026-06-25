from src.rectangle import Rectangle
from src.square import Square
import pytest


@pytest.mark.parametrize(
    ("side_a", "side_b", "area", "perimeter"),
    [
        pytest.param(10, 7, 70, 34, marks=[pytest.mark.positive], id='integer'),
        pytest.param(5.5, 10.35, 56.92, 31.7, marks=[pytest.mark.positive], id='float')
    ]
)
def test_rectangle_positive_sides(side_a, side_b, area, perimeter):
    r = Rectangle(side_a, side_b)
    assert r.area == area, f"The Area result was just calculated does not corresponds according to side values: side_a = {r.side_a} and side_b = {r.side_b}"
    assert r.perimeter == perimeter, f"The Perimeter result was just calculated does not corresponds according to side values: side_a = {r.side_a} and side_b = {r.side_b}"


@pytest.mark.parametrize(
    ("side_a", "side_b"),
    [
        pytest.param(3.3, 0, marks=[pytest.mark.negative], id='zero'),
        pytest.param(-3, 5, marks=[pytest.mark.negative], id='below zero')
    ]
)
def test_rectangle_negative_int(side_a, side_b):
    with pytest.raises(ValueError, match="Side parameters must be above zero"):
        Rectangle(side_a, side_b)


@pytest.mark.parametrize(
    ("side_a", "side_b"),
    [
        pytest.param('3', 5, marks=[pytest.mark.negative], id='int in quotes'),
        pytest.param(15, 'this_is_string', marks=[pytest.mark.negative], id='letter in quotes')
    ]
)
def test_rectangle_string(side_a, side_b):
    with pytest.raises(TypeError, match='Side parameters types must be: "int" or "float"'):
        Rectangle(side_a, side_b)


@pytest.mark.parametrize(
    ("side_a_rectangle_1", "side_b_rectangle_1", "side_a_rectangle_2", "side_b_rectangle_2", "side_square", "sum_area_rec1_rec2", "sum_area_rec1_sq"),
    [
        pytest.param(8, 11, 50, 7, 10, 438, 188, marks=[pytest.mark.positive], id='add area, integer'),
        pytest.param(10.1, 14.44, 5.5, 2.2, 6.6, 157.94, 189.4, marks=[pytest.mark.positive], id='add area, float')
    ]
)
def test_rectangle_add_areas(side_a_rectangle_1, side_b_rectangle_1, side_a_rectangle_2, side_b_rectangle_2, side_square, sum_area_rec1_rec2, sum_area_rec1_sq):
    test_rectangle_1 = Rectangle(side_a_rectangle_1, side_b_rectangle_1)
    test_rectangle_2 = Rectangle(side_a_rectangle_2, side_b_rectangle_2)
    test_square = Square(side_square)
    assert test_rectangle_1.add_area(test_rectangle_2) == sum_area_rec1_rec2, "The sum area of test_rectangle_1 and test_rectangle_2 does not correspond to calculations"
    assert test_rectangle_1.add_area(test_square) == sum_area_rec1_sq, "The sum area of test_rectangle_1 and test_square does not correspond to calculations"