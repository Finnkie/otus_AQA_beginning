import math
from src.figure import Figure


class Circle(Figure):

    def __init__(self, radius: int | float):
        self.radius = radius
        if not isinstance(radius, (int, float)):
            raise TypeError(f'Radius must be type: "int" or "float". Yours: {type(radius)}')
        if radius <= 0:
            raise ValueError(f'Radius value must be above zero. Yours: {radius}')


    @property
    def area(self):
        return round((math.pi * self.radius ** 2), 2)
    

    @property
    def perimeter(self):
        return round((2 * math.pi * self.radius), 2)
    
