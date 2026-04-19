from factory.shape_factory import ShapeFactory
from enums.shape_type import ShapeType

def main():
    factory = ShapeFactory()

    shape1 = factory.get_shape(ShapeType.CIRCLE)
    print(shape1.draw())

    shape2 = factory.get_shape(ShapeType.SQUARE)
    print(shape2.draw())

if __name__ == "__main__":
    main()

