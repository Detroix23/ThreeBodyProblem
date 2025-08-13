"""
THREE BODY PROBLEM.
Maths functions.
"""

import math

class Vector2D:
    """
    Define a simple 2D vector with methods
    """
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
    
    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> None:
        magnitude: float = self.magnitude
        self.x = self.x / magnitude
        self.y = self.y / magnitude
        
        assert(self.magnitude != 1)
        
    def to_list(self) -> list[float]:
        return [self.x, self.y]
    
    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}
    
    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

