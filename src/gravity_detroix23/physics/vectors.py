"""
# Gravity.
src/gravity/physics/vectors.py  
"""
import math
import pyxel
from typing import Self, Union

Scalar = Union[int, float]
ScalarOrVector = Union[Scalar, 'Vector2D']

class Vector2D:
    """
    # Simple mutable `float` `Vector2D`.
    """
    x: float
    y: float

    def __init__(self, x: Scalar, y: Scalar) -> None:
        self.x = float(x)
        self.y = float(y)

        return
    
    @staticmethod
    def duplicate(value: Scalar) -> 'Vector2D':
        """
        Create a `Vector2D(value, value)` from a single value.
        """
        return Vector2D(value, value)

    @staticmethod
    def null() -> 'Vector2D':
        """
        Creates a `(0; 0)` vector.
        """
        return Vector2D(0.0, 0.0)

    def __str__(self) -> str:
        """
        Formatted `str`.
        """
        return f"({self.x};{self.y})"

    def __repr__(self) -> str:
        """
        `exec` compatible `str`.
        """
        return f"Vector2D(x={self.x}, y={self.y})"

    def __add__(self, value: ScalarOrVector) -> 'Vector2D':
        """
        Add values to the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        if isinstance(value, Vector2D):
            return Vector2D(
                self.x + value.x, 
                self.y + value.y,
            )
        elif isinstance(value, float) or isinstance(value, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            return Vector2D(
                self.x + float(value), 
                self.y + float(value),
            )
        else:
            return NotImplemented


    def __radd__(self, value: ScalarOrVector) -> 'Vector2D':
        """
        Swap addition members for `__add__`.  
        """
        return (
            self.__add__(value)
            if value != 0
            else self
        )
    
    def __sub__(self, value: ScalarOrVector) -> 'Vector2D':
        """
        Add values to the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        if isinstance(value, Vector2D):
            return Vector2D(
                self.x - value.x, 
                self.y - value.y,
            )
        elif isinstance(value, float) or isinstance(value, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            return Vector2D(
                self.x - float(value), 
                self.y - float(value),
            )
        else:
            return NotImplemented

    def __rsub__(self, value: ScalarOrVector) -> 'Vector2D':
        """
        Swap addition members for `__add__`.  
        """
        return (
            self.__sub__(value)
            if value != 0
            else self
        )

    def __mul__(self, factor: Scalar) -> 'Vector2D':
        """
        Multiply the values of the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        return Vector2D(
            self.x * float(factor), 
            self.y * float(factor),
        )
    
    __rmul__ = __mul__

    def __truediv__(self, factor: Scalar) -> 'Vector2D':
        """
        Divide all value of the vector, emulating numeric objects.
        Do not update the content of the vector
        """
        return Vector2D(
            self.x / float(factor), 
            self.y / float(factor),
        )

    __rtruediv__ = __truediv__

    def copy(self) -> 'Vector2D':
        """
        Return a true copy of `self`.
        """
        return Vector2D(
            self.x,
            self.y,
        )
    
    def magnitude2(self) -> float:
        """
        Return the length _squared_ of the vector.
        """
        return self.x * self.x + self.y * self.y

    def magnitude(self) -> float:
        """
        Return the length of the vector.
        """
        return math.sqrt(self.magnitude2())

    def __abs__(self) -> float:
        return self.magnitude()

    def normalize(self) -> 'Vector2D':
        """
        Update the vector so that its magnitude is 1.  
        """
        magnitude: float = self.magnitude()
        if magnitude > 0.0:
            self.x = self.x / magnitude
            self.y = self.y / magnitude

        return self
        
    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def to_list(self) -> list[float]:
        return [self.x, self.y]
    
    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y} 

    def draw_on(
        self, 
        x: float, 
        y: float, 
        size: float, 
        color: int,
    ) -> None:
        if not self.is_zero(): 
            pyxel.line(
                x, 
                y, 
                x + self.x * size, 
                y + self.y * size, 
                col=color,
            )

        return

    def add(self, value: ScalarOrVector) -> Self:
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
    
    def sub(self, value: ScalarOrVector) -> Self:
        """
        Add values to the vector.
        Do update the value of the vector.
        """
        if isinstance(value, Vector2D):
            self.x -= value.x
            self.y -= value.y
        else:
            self.x -= float(value)
            self.y -= float(value)

        return self

    def multiply(self, factor: Scalar) -> Self:
        """
        Multiply the values of the vector.
        Do update the value of the vector.
        """
        self.x = self.x * float(factor)
        self.y = self.y * float(factor)

        return self

    def div(self, factor: Scalar) -> Self:
        """
        Divide all value of the vector.
        Do update the value of the vector. 
        """
        self.x = self.x / float(factor)
        self.y = self.y / float(factor)
        
        return self
    
    def dot(self, other: 'Vector2D') -> float:
        """
        Compute the dot-product using the analytic way: a.x * b.x + a.y * b.y.
        Do not update the content of the vector
        """
        return self.x * other.x + self.y * other.y
    
    def zero(self) -> None:
        """
        Set all coordinate to zero.  
        """
        self.x = 0.0
        self.y = 0.0
        return

    def is_zero(self) -> bool:
        """
        Returns if the `Vector2D` is a 0 vector.
        """
        return math.isclose(self.x, 0.0) and math.isclose(self.y, 0.0)

    def is_close(self, other: 'Vector2D', offset: Scalar = 0.05) -> bool:
        """
        Return if the `other` vector if close enough in `offset`.   
        Linear.
        """
        return (
            abs(self.x - other.x) < float(offset) 
            and abs(self.y - other.y) < float(offset)
        )


class Size:
    """
    # `Size`, a (`int`; `int`) couple.
    """
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        return


def dot_product(a: Vector2D, b: Vector2D) -> float:
    """
    Given two vector, compute their dot product.
    """
    return a.dot(b)

def orthogonal(vector: Vector2D) -> Vector2D:
    """
    Returns a π/2 rotated vector.
    """
    return Vector2D(
        -vector.y,
        vector.x,
    )
