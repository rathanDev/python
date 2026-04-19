from factory.shape import Shape

# Concrete products

class Circle(Shape):
    def draw(self):
        return "Drawing a circle"