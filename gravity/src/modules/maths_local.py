"""
THREE BODY PROBLEM.
Maths functions.
"""

import math
import pyxel
from typing_extensions import Self

class Vector2D:
    """
    Define a simple 2D vector with methods
    """
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
    
    def __str__(self) -> str:
        return f"x = {self.x}, y = {self.y}"

    def __repr__(self) -> str:
        return f"Vector2D: x = {self.x}, y = {self.y}, magnitude={self.magnitude}; "

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> None:
        magnitude: float = self.magnitude
        self.x = self.x / magnitude
        self.y = self.y / magnitude

        assert(0.9 < self.magnitude < 1.1)
    
        
    def to_list(self) -> list[float]:
        return [self.x, self.y]
    
    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y} 
    
    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def draw_on(self, x: float, y: float, size: float, color: int) -> None:
        if not (math.isclose(self.x, 0) and math.isclose(self.y, 0)): 
            pyxel.line(x, y, x + self.x * size, y + self.y * size, col=color)

    def add(self, value: float|int|Self) -> Self:
        """
        Add values to the vector.
        Do update the value of the vector.
        """
        if isinstance(value, Vector2D):
            self.x += value.x
            self.y += value.y
        else:
            self.x += float(value)
            self.y += float(value)
        return self
    
    def sub(self, value: float|int|Self) -> Self:
        """
        Add values to the vector.
        Do update the value of the vector.
        """
        if isinstance(value, Vector2D):
            self.x = self.x - value.x
            self.y = self.y - value.y
        else:
            self.x -= float(value)
            self.y -= float(value)
        return self

    def mult(self, factor: float) -> Self:
        """
        Multiply the values of the vector.
        Do update the value of the vector.
        """
        self.x = self.x * factor
        self.y = self.y * factor
        return self

    def div(self, factor: float) -> Self:
        """
        Divide all value of the vector.
        Do update the value of the vector. 
        """
        self.x = self.x / factor
        self.y = self.y / factor
        return self
    
    def dot(self, other: Self) -> float:
        """
        Compute the dot-product using the analytic way: a.x * b.x + a.y * b.y.
        Do not update the content of the vector
        """
        return self.x * other.x + self.y * other.y

    def __add__(self, value: float|int|Self) -> Self:
        """
        Add values to the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        if isinstance(value, Vector2D):
            return Vector2D(self.x + value.x, self.y + value.y) # type: ignore
        else:
            return Vector2D(self.x + float(value), self.y + float(value)) # type: ignore

    def __sub__(self, value: float|int|Self) -> Self:
        """
        Add values to the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        if isinstance(value, Vector2D):
            return Vector2D(self.x - value.x, self.y - value.y) # type: ignore
        else:
            return Vector2D(self.x - float(value), self.y - float(value)) # type: ignore
    
    def __mul__(self, factor: float) -> Self:
        """
        Multiply the values of the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        return Vector2D(self.x * factor, self.y * factor) # type: ignore


    def __truediv__(self, factor: float) -> Self:
        """
        Divide all value of the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        return Vector2D(self.x / factor, self.y / factor) # type: ignore



def dot_product(a: Vector2D, b: Vector2D) -> float:
    """
    Given two vector, compute their dot product.
    """
    return a.dot(b)