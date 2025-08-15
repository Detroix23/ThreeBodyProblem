"""
THREE BODY PROBLEM.
Maths functions.
"""

import math
import pyxel


class Vector2D:
    """
    Define a simple 2D vector with methods
    """
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
    
    def __str__(self) -> str:
        return f"Vector2D: x = {self.x}, y = {self.y}"
        
    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> None:
        magnitude: float = self.magnitude
        self.x = self.x / magnitude
        self.y = self.y / magnitude
    
        
    def to_list(self) -> list[float]:
        return [self.x, self.y]
    
    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}
    
    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    
    def draw_on(self, x: float, y: float, size: float, color: int) -> None:
        if not (math.isclose(self.x, 0) and math.isclose(self.y, 0)): 
            pyxel.line(x, y, x + self.x * size, y + self.y * size, col=color)

    def mult(self, factor: float) -> None:
        """
        Multiply the values of the vector
        """
        self.x = self.x * factor
        self.y = self.y * factor
        
    def add(self, value: float) -> None:
        """
        Add values to the vector
        """
        self.x = self.x + value
        self.y = self.y + value
