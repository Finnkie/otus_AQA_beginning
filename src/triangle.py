import math
from figure import Figure


class Triangle(Figure):

    def __init__(self, side_a: int | float, side_b: int | float, side_c: int | float):
        self.side_a, self.side_b, self.side_c = side_a, side_b, side_c
        if not isinstance(side_a, (int, float)) or not isinstance (side_b, (int, float))or not isinstance (side_c, (int, float)):
            raise TypeError('\n\nRadius must be type: "int" or "float"')
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError(f'\n\nSide parameter values must be above zero.\nYour values: side_a: {side_a}\tside_b: {side_b}\tside_c: {side_c}')
        if side_a + side_b <= side_c or side_b + side_c <= side_a or side_a + side_c <= side_b:
            raise ValueError(f'\n\nTriangle with values {side_a}, {side_b}, {side_c} does not exist! \nIn a triangle, the sum of any two side values must be strictly greater than third side value.')


    @property
    def area(self):
        # Полупериметр для формулы Герона:
        p = self.perimeter / 2
        # Площадь по формуле Герона:
        return round(math.sqrt(p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c)), 2)
    

    @property
    def perimeter(self):
        return round((self.side_a + self.side_b + self.side_c), 2)
    
