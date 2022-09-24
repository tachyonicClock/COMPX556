class Rectangle():
    """A rectangle"""

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def quarters(self):
        """Split the square into four equal squares"""
        return [
            Rectangle(self.x, self.y, self.width/2, self.height/2),
            Rectangle(self.x + self.width/2, self.y,
                      self.width/2, self.height/2),
            Rectangle(self.x, self.y + self.height /
                      2, self.width/2, self.height/2),
            Rectangle(self.x + self.width/2, self.y +
                      self.height/2, self.width/2, self.height/2)
        ]

    def center(self):
        """Return the center of the square"""
        return (self.x + self.width/2, self.y + self.height/2)

    def __repr__(self) -> str:
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"
