from src.rectangle import Rectangle
from src.figure import Figure
from src.circle import Circle
from src.triangle import Triangle
import pytest


@pytest.mark.parametrize(
    ("radius", "area", "perimeter"),
    [   
        pytest.param(38, 4536.46, 238.76, marks=[pytest.mark.positive], id='integer'),
        pytest.param(3.3, 34.21, 20.73, marks=[pytest.mark.positive], id='float')
    ]
)
def test_circle_positive_radiuses(radius, area, perimeter):
    c = Circle(radius)
    assert c.area == area, f"The Area result was just calculated does not corresponds to the calculating one: radius = {radius}"
    assert c.perimeter == perimeter, f"The Perimeter result was just calculated does not corresponds to the calculating one: radius = {radius}"


@pytest.mark.parametrize(
    ("radius"),
    [
        pytest.param(0, marks=[pytest.mark.negative], id='zero'),
        pytest.param(-133, marks=[pytest.mark.negative], id='below zero')
    ]
)
def test_rectangle_negative_int(radius):
    with pytest.raises(ValueError, match="Radius value must be above zero"):
        Circle(radius)


@pytest.mark.parametrize(
    ("radius"),
    [
        pytest.param('54', marks=[pytest.mark.negative], id='int in quotes'),
        pytest.param('this_is_string', marks=[pytest.mark.negative], id='letter in quotes')
    ]
)
def test_rectangle_string(radius):
    with pytest.raises(TypeError, match='Radius must be type: "int" or "float".'):
        Circle(radius)


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
    test_rec = Rectangle(side_a_rectangle, side_b_rectangle)
    test_tri = Triangle(side_a_triangle, side_b_triangle, side_c_triangle)
    assert test_cir.add_area(test_rec) == area_cir_rec, "The sum area of a circle and rectangle does not correspond to calculations"
    assert test_cir.add_area(test_tri) == area_cir_tri, "The sum area of a circle and triangle does not correspond to calculations"