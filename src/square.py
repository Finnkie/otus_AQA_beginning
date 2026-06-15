from rectangle import Rectangle


class Square(Rectangle):

    def __init__(self, side_a: int | float):
        self.side_a, self.side_b = side_a, side_a
        if side_a <= 0:
            raise ValueError(f'\n\nSide parameter value must be above zero.\nYour value: {side_a}')

        if not isinstance(side_a, (int, float)):
            raise TypeError('Side parameters must be type: "int" or "float"')
        


