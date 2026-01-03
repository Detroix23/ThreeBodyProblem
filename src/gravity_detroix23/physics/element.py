"""
THREE BODY PROBLEM.
element.py
"""
import math
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import gravity_detroix23.app.board as board

from gravity_detroix23.modules import (
    defaults,
)
from gravity_detroix23.physics import (
    maths,
    trails,
)
from gravity_detroix23.app import (
    drawing,
    support,
)

class Element:
    """
    Define a stellar element
    """
    CHECK_RADIUS: int = 100
    SPRITE_POSITION: maths.Vector2D = maths.Vector2D(16, 0)
    SPRITE_SIZE: maths.Vector2D = maths.Vector2D(16, 16)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = defaults.SPRITE_COLKEY
    SPRITE_SIZE_FACTOR: float = 1/16

    trail: trails.Trail
    displacement: maths.Vector2D

    def __init__(
        self, 
        board: board.Board, 
        mass: int, 
        position: maths.Vector2D, 
        velocity: maths.Vector2D,
        color: int = 5, 
        size: int = 2, 
        name: str = "",
    ) -> None:
        """
        Create an `Element`.
        """
        self.board: board.Board = board
        self.mass: float = mass  
        self.position: maths.Vector2D = position
        self.trail = trails.Trail(self.board.app, 5000, support.Color.WHITE)

        self.velocity: maths.Vector2D = velocity
        self.force_vector: maths.Vector2D = maths.Vector2D(0, 0)
        self.collisions: list[Element] = []
        self.displacement = maths.Vector2D(0, 0)

        # Drawing sprite will use the pyxres template, else, a square will be drawn.
        self.draw_sprite: bool = True
        self.size: int = size
        self.color: int = color
        self.name: str = name

    def __str__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position.x}; y={self.position.y}, Mass: m={self.mass}, \
Force: x={self.force_vector.x}; y={self.force_vector.y}."
    
    def __repr__(self) -> str:
        return f"Element(name={self.name}, position={self.position}, mass={self.mass}, velocity={self.force_vector}, \
color={self.color}, size={self.size})"
    
    def distance_to(self, target: 'Element') -> float:
        """
        Compute distance between `self and the `target` element.
        """
        return math.sqrt((target.position.x - self.position.x) ** 2 + (target.position.y - self.position.y) ** 2)
    
    def gravitational_force_from(self, target: 'Element') -> maths.Vector2D:
        """
        Find the gravitational force vector between `self` and `target`.
        """
        direction: int = 1
        # Direction
        vector_distance: maths.Vector2D = maths.Vector2D(x = target.position.x - self.position.x, y = target.position.y - self.position.y)
        vector_distance.normalize()
        # Distance
        distance: float = self.distance_to(target)
        # Limit artificially distance and prevent division by 0
        distance_min: float = ((self.size + 1) / 2 + (target.size + 1) / 2)
        if distance < distance_min:
            distance = distance_min
        
        # F force value
        force: float = (self.board.gravitational_constant * target.mass) / (distance ** (2 + self.board.exponent_softener))
        # Force vector
        vector_force: maths.Vector2D = maths.Vector2D(x = force * vector_distance.x * direction, y = force * vector_distance.y * direction)
        # Watch for overshot of planets
        velocity_next: maths.Vector2D = maths.Vector2D(
            x = self.velocity.x + self.force_vector.x / (self.mass * self.board.mass_softener),
            y = self.velocity.y + self.force_vector.y / (self.mass * self.board.mass_softener)
        )
        if velocity_next.magnitude >= distance:
            direction = -1
            velocity_next_magnitude: float = velocity_next.magnitude
            velocity_next.normalize()
            velocity_next.multiply((velocity_next_magnitude - distance) * direction)
        
        
        return vector_force


    def move(self) -> None:
        """
        Move the elem, according to force vector at a scale (mass) and checking collision.
        """ 
        # Apply force.
        self.velocity.add(self.force_vector / (self.mass * self.board.mass_softener))

        # Apply velocity.
        self.position.add(self.velocity)

        # Displacement.
        self.position.add(self.displacement) 
        self.displacement.zero()

        # Update trail.
        if self.trail and not self.position.is_close(self.trail.first, 1):
            self.trail.push(self.position.copy())

    def compute_position(self) -> maths.Vector2D:
        initial: maths.Vector2D = maths.Vector2D(
            self.position.x - (self.size / (2 * self.size * self.SPRITE_SIZE_FACTOR)),
            self.position.y - (self.size / (2 * self.size * self.SPRITE_SIZE_FACTOR)),
        )
        
        return self.board.camera.transform(initial)

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        # Draw on computed values
        size: int = int(self.size)
        position: maths.Vector2D = maths.Vector2D(
            int(self.position.x),
            int(self.position.y)
        )
        if self.draw_sprite:
            position: maths.Vector2D = self.compute_position()
            pyxel.blt(
                x=position.x, 
                y=position.y, 
                img=self.SPRITE_IMAGE, 
                u=self.SPRITE_POSITION.x,
                v=self.SPRITE_POSITION.y,
                w=self.SPRITE_SIZE.x,
                h=self.SPRITE_SIZE.y,
                colkey=self.SPRITE_COLKEY,
                scale=self.size * self.SPRITE_SIZE_FACTOR * self.board.camera.zoom
            )
        else:
            # Main rectangle
            pyxel.rect(position.x - size / 2, position.y - size / 2, size, size, col=self.color)
            # Outline
            pyxel.rectb(position.x - size / 2, position.y - size / 2, size, size, col=7)
        
            # Center
            drawing.draw_point(int(position.x), int(position.y), 16)
    