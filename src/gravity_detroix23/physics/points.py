"""
# Gravity.
src/gravity_detroix23/physics/points.py
"""
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app.board import Board
from gravity_detroix23.physics.vectors import Vector2D


class Point:
    """
    Point of the grid 
    """
    board: 'Board'
    position: Vector2D
    
    def __init__(self, position: Vector2D, board: 'Board') -> None:
        self.position = position
        self.board: 'Board' = board
        self.force: Vector2D = Vector2D(0, 0)
        
    def distance2(self, target: Vector2D) -> float:
        """
        Compute the distance _squared_ between `self` and `target`.
        Doesn't do a square root.
        """
        physical_position: Vector2D = self.board.camera.transform(self.position, True)
        return (target - physical_position).magnitude2()

    def distance(self, target: Vector2D) -> float:
        """
        Compute distance between `self` point and the `target` point.
        """
        return math.sqrt(self.distance2(target))
    
    def gravitational_force_from(self, target: Vector2D, target_mass: float) -> Vector2D:
        """
        Find the gravitational force vector between `self` point and `target` point.
        """
        physical_position: Vector2D = self.board.camera.transform(self.position, True)
        # Direction
        vector_distance: Vector2D = Vector2D(target.x - physical_position.x, target.y - physical_position.y)
        vector_distance.normalize()
        # Distance
        distance: float = self.distance(target)
        if distance < 1.0:
            distance = 1.0
        
        # F force value
        force: float = (self.board.gravitational_constant * target_mass) / (distance ** (2 + self.board.exponent_softener))
        if force > distance:
            force = distance
        # Force vector
        vector_force: Vector2D = Vector2D(force * vector_distance.x, force * vector_distance.y)
        
        return vector_force
