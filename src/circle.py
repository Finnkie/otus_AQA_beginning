import math
from src.figure import Figure


class Circle(Figure):

    def __init__(self, radius: int | float):
        self.radius = radius
        if not isinstance(radius, (int, float)):
            raise TypeError('\n\nRadius must be type: "int" or "float"')
        if radius <= 0:
            raise ValueError(f'\n\nRadius value must be above zero.\nYour value: {radius}')


    @property
    def area(self):
        return round((math.pi * self.radius ** 2), 2)
    

    @property
    def perimeter(self):
        return round((2 * math.pi * self.radius), 2)
    
