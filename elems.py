"""
THREE BODY PROBLEM
Definitions of elements
"""

#Local

import math

from maths_local import *
import main


class Elem:
    """
    Define a stellar element
    """
    CHECK_RADIUS = 100
    
    def __init__(
        self, BOARD: main.Board, mass: int, position: Vector2D, velocity: Vector2D,
        color: int = 5, size: int = 2, name: str = "",
    ) -> None:
        """
        Creation of the elem, with "mass, vInit, xStart, yStart, color=5, size=2".
        """
        self.BOARD: main.Board = BOARD
        self.mass: float = mass  
        self.position: Vector2D = position
        
        self.velocity: Vector2D = velocity
        self.force_vector: Vector2D = Vector2D(x = 0, y = 0)

        self.size: int = size
        self.color: int = color
        self.name: str = name

    def __str__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position.x}; y={self.position.y}, Mass: m={self.mass}, Force: x={self.force_vector.x}; y={self.force_vector.y}."
    
    def __repr__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position.x}; y={self.position.y}, Mass: m={self.mass}, Force: x={self.force_vector.x}; y={self.force_vector.y}."
    
    def distance_to(self, target_position: Vector2D) -> float:
        """
        Compute distance between this elem and the target elem
        """
        return math.sqrt((target_position.x - self.position.x) ** 2 + (target_position.y - self.position.y) ** 2)
    
    def gravitational_force_from(self, target_position: Vector2D, target_size: int, target_mass: float) -> Vector2D:
        """
        Find the gravitational force vector
        """
        # Direction
        vector_distance: Vector2D = Vector2D(x = target_position.x - self.position.x, y = target_position.y - self.position.y)
        vector_distance.normalize()
        # Distance (limited)
        distance: float = self.distance_to(target_position)
        if distance < ((self.size + 1) / 2 + (target_size + 1) / 2):
            distance = ((self.size + 1) / 2 + (target_size + 1) / 2)
        # F force value
        force: float = (self.BOARD.gravitational_constant * target_mass) / (distance ** (2 + self.BOARD.exponent_softener))
        # Force vector
        vector_force: Vector2D = Vector2D(x = force * vector_distance.x, y = force * vector_distance.y)

        return vector_force

    def does_collide_with(self, target_position: Vector2D) -> bool:
        return False

    def move(self) -> None:
        """
        Move the elem, according to force vector at a scale (mass) and checking collision
        """
        # Apply force
        self.velocity = Vector2D(
            x = self.velocity.x + self.force_vector.x / (self.mass * self.BOARD.mass_softener),
            y = self.velocity.y + self.force_vector.y / (self.mass * self.BOARD.mass_softener)
        )
        
        # Apply velocity
        self.position = Vector2D(
            x = self.position.x + self.velocity.x,
            y = self.position.y + self.velocity.y
        )

        # Check edges
        # Disabled for now
        """
        for axis1 in (0, 1):
            axis2: int = abs(axis1 - 1)
            force_vector_list: list[float] = self.force_vector.to_list()
            position_list: list[float] = self.position.to_list()

            if self.position[axis1] + self.size / 2 >= self.BOARD.width:
                if self.BOARD.edges == "bounce":
                    force_vector_list[axis1] = self.force_vector[axis1] * -self.BOARD.bounce_factor
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board and count reflexion
                    position_list[axis1] = 2 * self.BOARD.width - self.size / 2 - self.position[axis1]

                elif self.BOARD.edges == "hard":
                    force_vector_list[axis1] = 0.0
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board
                    position_list[axis1] = self.BOARD.width - self.size / 2
                    
            elif self.position[axis1] <= 0:
                if self.BOARD.edges == "bounce":
                    force_vector_list[axis1] = self.force_vector[axis1] * -self.BOARD.bounce_factor
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board and count reflexion
                    position_list[axis1] = 0

                elif self.BOARD.edges == "hard":
                    force_vector_list[axis1] = 0.0
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board
                    position_list[axis1] = 0


            self.force_vector = (force_vector_list[0], force_vector_list[1])
            self.position = (position_list[0], position_list[1])
        """

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        
        # Draw on computed values
        size: int = int(self.size * self.BOARD.zoom)
        position_x: int = int((self.position.x + self.BOARD.camera_x) * self.BOARD.zoom)
        position_y: int = int((self.position.y + self.BOARD.camera_y) * self.BOARD.zoom)

        main.pyxel.rect(position_x - size / 2, position_y - size / 2, size, size, col=self.color)
        main.pyxel.rect(position_x, position_y, 1, 1, col=self.color + 1)





if __name__ == "__main__":
    print("THREE BODY PROBLEM - Libraries.")
    print("Elems.")
