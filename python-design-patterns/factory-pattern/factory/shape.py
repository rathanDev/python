from abc import ABC, abstractmethod

# Abstract product
class Shape(ABC):

    @abstractmethod
    def draw(self):
        pass