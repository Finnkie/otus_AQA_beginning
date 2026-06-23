from src.figure import Figure


class Rectangle(Figure):

    def __init__(self, side_a: int | float, side_b: int | float):
        self.side_a, self.side_b = side_a, side_b
        if not isinstance(side_a, (int, float)) or not isinstance (side_b, (int, float)):
            raise TypeError('Side parameters types must be: "int" or "float"')
        if side_a <= 0 or side_b <= 0:
            raise ValueError(f'Side parameters must be above zero.\nYour values: side_a: {side_a}\tside_b: {side_b}')


    @property
    def area(self):
        return round(self.side_a * self.side_b, 2)
    

    @property
    def perimeter(self):
        return round(2 *( self.side_a + self.side_b), 2)

