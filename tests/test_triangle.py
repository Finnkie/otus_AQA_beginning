from src.triangle import Triangle
from src.square import Square
from src.figure import Figure
from src.circle import Circle
import pytest


@pytest.mark.parametrize(
    ("side_a", "side_b", "side_c", "area", "perimeter"),
    [   
        pytest.param(3, 4, 5, 6, 12, marks=[pytest.mark.positive], id='integer'),
        pytest.param(5.7, 8.3, 10.1, 23.36, 24.1, marks=[pytest.mark.positive], id='float')
    ]
)
def test_circle_positive_radiuses(side_a, side_b, side_c, area, perimeter):
    tr = Triangle(side_a, side_b, side_c)
    assert tr.area == area, f"The Area result was just calculated does not corresponds to the calculating one, sides: {side_a}, {side_b}, {side_c}"
    assert tr.perimeter == perimeter, f"The Perimeter result was just calculated does not corresponds to the calculating one, sides: {side_a}, {side_b}, {side_c}"


@pytest.mark.parametrize(
    ("side_a", "side_b", "side_c"),
    [
        pytest.param(14, 0, 12.4, marks=[pytest.mark.negative], id='zero'),
        pytest.param(-3, 4, 5, marks=[pytest.mark.negative], id='below zero')
    ]
)
def test_rectangle_negative_int(side_a, side_b, side_c):
    with pytest.raises(ValueError, match="Sides value must be above zero. Yours: {side_a}, {side_b}, {side_c}"):
        Triangle(side_a, side_b, side_c)


@pytest.mark.parametrize(
    ("side_a", "side_b", "side_c"),
    [
        pytest.param('3', 4, 5, marks=[pytest.mark.negative], id='int in quotes'),
        pytest.param('this_is_string', 4, 5, marks=[pytest.mark.negative], id='letter in quotes')
    ]
)
def test_rectangle_string(side_a, side_b, side_c):
    with pytest.raises(TypeError, match='Sides value must be type: "int" or "float"'):
        Triangle(side_a, side_b, side_c)


@pytest.mark.parametrize(
    ("side_a", "side_b", "side_c"),
    [
        pytest.param(3, 6, 15, marks=[pytest.mark.negative], id='not excist'),
        pytest.param(218, 0.2, 99999, marks=[pytest.mark.negative], id='not excist')
    ]
)
def test_rectangle_string(side_a, side_b, side_c):
    with pytest.raises(TypeError, match='Triangle with values {side_a}, {side_b}, {side_c} does not exist!'):
        Triangle(side_a, side_b, side_c)


@pytest.mark.parametrize(
    ("radius", "side_a_rectangle", "side_b_rectangle","side_a_triangle", "side_b_triangle", "side_c_triangle", "area_cir_tri", "area_cir_rec"),
    [
        pytest.param(11, 2, 16, 3, 4, 5, 386.13, 412.13, marks=[pytest.mark.positive], id='add area, integer'),
        pytest.param(15.2, 2.3, 14.9, 5.7, 8.2, 10.1, 749.19, 760.1, marks=[pytest.mark.positive], id='add area, float'),
        pytest.param(8.5, 7, 13.2, 6.8, 9.3, 11.5, 258.60, 319.38, marks=[pytest.mark.positive], id='add area, mixed')
    ]
)
def test_rectangle_add_areas(radius, side_a_rectangle, side_b_rectangle, side_a_triangle, side_b_triangle, side_c_triangle, area_cir_tri, area_cir_rec):
    test_cir = Circle(radius)
    test_rec = Square(square_side)
    test_tri = Triangle(side_a_tri, side_b_tri, side_c_tri)
    assert test_cir.add_area(test_rec) == area_cir_rec, "The sum area of a circle and rectangle does not correspond to calculations"
    assert test_cir.add_area(test_tri) == area_cir_tri, "The sum area of a circle and triangle does not correspond to calculations"