"""
# THREE BODY PROBLEM
Settings and enumeration file
"""
import enum

from gravity_detroix23.physics.maths import *

# Gravity.
class Edge(enum.Enum):
    NONE = 1
    HARD = 2
    BOUNCE = 3
    TOR = 4
    
class SimMode(enum.Enum):
    RANDOM = 1
    CONFIG = 2
    DEFAULT = 3 

class CollisionsBehaviour(enum.Enum):
    NONE = 1
    COLLIDE = 2
    COLLIDE_WITH_FUSION = 3
    COLLIDE_WITH_BUMP = 4

# Inputs.
class InputElem:
    """
    Named tuple of the input infos.
    """
    def __init__(self, mass: int, position: Vector2D, name: str, size: int, velocity: Vector2D) -> None:
        self.mass: int = mass
        self.position: Vector2D = position
        self.name: str = name
        self.size: int = size
        self.velocity: Vector2D = velocity

    def __repr__(self) -> str:
        return f"{self.__class__!s}({self.__dict__!r})"
    
    def __str__(self) -> str:
        return f"Elem: {self.name}, position: x={self.position.x}, y={self.position.y}, size={self.size}, velocity: x={self.velocity.x}, y={self.velocity.y}"



# Defaults.
DEFAULT_SYSTEM: dict[str, InputElem] = {
    # Mass, position, name, size, velocity.
    # system_input["Plan1"] = InputElem(10500, Vector2D(445, 560), "Plan1", 100, Vector2D(0, 0)),
    "Plan2": InputElem(2000, Vector2D(580, 450), "Plan2", 64, Vector2D(0, -1)),
    "Plan3": InputElem(1000, Vector2D(400, 400), "Plan3", 48, Vector2D(0, -3)),
    "Plan4": InputElem(200, Vector2D(300, 350), "Plan4", 8, Vector2D(2, 0)),
}

