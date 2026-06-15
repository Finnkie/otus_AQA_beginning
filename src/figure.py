from abc import ABC, abstractmethod


class Figure(ABC):

    @property
    @abstractmethod
    def area(self):
        pass


    @property
    @abstractmethod
    def perimeter(self):
        pass


    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise TypeError('\nArgument must be a child Object of the abstract class Figure')
        return self.area + figure.area

