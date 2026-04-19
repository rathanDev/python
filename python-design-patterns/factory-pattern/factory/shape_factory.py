from factory.shape import Shape
from factory.circle import Circle
from factory.square import Square
from enums.shape_type import ShapeType

class ShapeFactory:

    @staticmethod
    def get_shape(shape_type: str) -> Shape:
        if shape_type == ShapeType.CIRCLE:
            return Circle()
        elif shape_type == ShapeType.SQUARE:
            return Square()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
