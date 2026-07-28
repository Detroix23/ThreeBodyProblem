"""
# THREE BODY PROBLEM
Settings and enumeration file
"""
import enum

from gravity_detroix23.physics.vectors import Vector2D

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


class CollisionsBehavior(enum.Enum):
    NONE = 1
    COLLIDE = 2
    COLLIDE_WITH_FUSION = 3
    COLLIDE_WITH_BUMP = 4


class InputElement:
    """
    Named tuple of the input infos.
    """
    def __init__(
        self, 
        mass: int, 
        position: Vector2D, 
        name: str, 
        size: int, 
        velocity: Vector2D
    ) -> None:
        self.mass: int = mass
        self.position: Vector2D = position
        self.name: str = name
        self.size: int = size
        self.velocity: Vector2D = velocity

    def __repr__(self) -> str:
        return f"{self.__class__!s}({self.__dict__!r})"
    
    def __str__(self) -> str:
        return (
            f"{self.name} position={self.position} " 
            f"size={self.size} velocity={self.velocity}"
        )
