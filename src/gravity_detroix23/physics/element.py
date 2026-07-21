"""
# Gravity.
src/gravity_detroix23/physics/element.py
"""
import math
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app.board import Board 

from gravity_detroix23.modules import defaults, entity
from gravity_detroix23.physics import trails, vectors
from gravity_detroix23.app import drawing

class Element(entity.Entity):
    """
    Define a stellar element
    """
    CHECK_RADIUS: int = 100
    SPRITE_POSITION: vectors.Vector2D = vectors.Vector2D(16, 0)
    SPRITE_SIZE: vectors.Vector2D = vectors.Vector2D(16, 16)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = defaults.SPRITE_COLKEY
    SPRITE_SIZE_FACTOR: float = 1/16

    board: 'Board'
    mass: float
    displacement: vectors.Vector2D
    position: vectors.Vector2D
    velocity: vectors.Vector2D
    acceleration: vectors.Vector2D
    force_vector: vectors.Vector2D
    trail: trails.Trail
    collisions: list['Element']

    draw_sprite: bool
    size: int
    color: int
    name: str

    def __init__(
        self, 
        board: 'Board', 
        mass: int, 
        position: vectors.Vector2D, 
        velocity: vectors.Vector2D,
        color: int = 5, 
        size: int = 2, 
        name: str = "",
        trail_size: int = 5000
    ) -> None:
        """
        Create an `Element`.
        """
        self.board = board
        self.mass = mass  
        self.displacement = vectors.Vector2D(0.0, 0.0)
        self.position = position
        self.velocity = velocity
        self.acceleration = vectors.Vector2D(0.0, 0.0)
        self.force_vector = vectors.Vector2D(0.0, 0.0)
        self.collisions = []


        # Drawing sprite will use the pyxres template, else, a square will be drawn.
        self.trail = trails.Trail(
            self.board.app, 
            trail_size, 
            pyxel.COLOR_WHITE
        )
        self.draw_sprite = True
        self.size = size
        self.color = color
        self.name = name

    def __str__(self) -> str:
        return (
            f"Element({self.name}, position={self.position}, "
            f"mass: m={self.mass}, force={self.force_vector})"
        )

    def __repr__(self) -> str:
        return (
            f"Element(name={self.name}, position={self.position}, mass={self.mass}, "
            f"velocity={self.force_vector}, color={self.color}, size={self.size})"
        )
    
    def get_position(self) -> entity.Vector2D:
        return self.position

    def get_velocity(self) -> entity.Vector2D:
        return self.velocity
    
    def get_acceleration(self) -> entity.Vector2D:
        return self.acceleration
    
    def set_position(self, vector: entity.Vector2D) -> None:
        self.position = vector
        return
    
    def set_velocity(self, vector: entity.Vector2D) -> None:
        self.velocity = vector
        return 

    def set_acceleration(self, vector: entity.Vector2D) -> None:
        self.acceleration = vector
        return
    
    def distance2(self, target: 'Element') -> float:
        """
        Compute distance _squared_ between `self and the `target` element.
        Doesn't do a square root.
        """
        return (target.position - self.position).magnitude2()

    def distance(self, target: 'Element') -> float:
        """
        Compute distance between `self and the `target` element.
        """
        return math.sqrt(self.distance2(target))
    
    def gravitational_force_from(self, target: 'Element') -> vectors.Vector2D:
        """
        Find the gravitational force vector between `self` and `target`.
        """
        direction: int = 1
        # Direction
        vector_distance: vectors.Vector2D = vectors.Vector2D(
            target.position.x - self.position.x,
            target.position.y - self.position.y,
        )
        vector_distance.normalize()
        
        # Distance.
        distance2: float = self.distance2(target)
        # Limit artificially distance and prevent division by 0
        distance: float
        distance_min: float = (self.size + target.size + 2) / 2
        if distance2 < distance_min * distance_min:
            distance = distance_min
        else:
            distance = math.sqrt(distance2)

        # F force value
        force: float = (
            (self.board.gravitational_constant * target.mass) 
            / (distance ** (2 + self.board.exponent_softener))
        )
        
        # Force vector
        vector_force: vectors.Vector2D = vectors.Vector2D(
            force * vector_distance.x * direction,
            force * vector_distance.y * direction,
        )
        
        # Watch for overshot of planets
        velocity_next: vectors.Vector2D = (
            self.velocity
            + self.force_vector 
            / (self.mass * self.board.mass_softener)
        )

        if velocity_next.magnitude() >= distance:
            direction = -1
            velocity_next_magnitude: float = velocity_next.magnitude()
            velocity_next.normalize()
            velocity_next.multiply((velocity_next_magnitude - distance) * direction)
        
        return vector_force


    def update(self) -> None:
        """
        Move the elem, according to force vector at a scale (mass) and checking collision.
        """ 
        # Apply force.
        self.velocity.add(
            self.force_vector 
            / (self.mass * self.board.mass_softener)
        )

        # Apply velocity.
        self.position.add(self.velocity)

        # Displacement.
        self.position.add(self.displacement) 
        self.displacement.zero()

        # Update trail.
        if self.trail and not self.position.is_close(self.trail.first, 1):
            self.trail.push(self.position.copy())

    def compute_position(self) -> vectors.Vector2D:
        initial: vectors.Vector2D = vectors.Vector2D(
            self.position.x - 2 * self.SPRITE_SIZE_FACTOR,
            self.position.y - 2 * self.SPRITE_SIZE_FACTOR,
        )
        
        return self.board.camera.transform(initial)

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        # Draw on computed values.
        size: int = int(self.size)
        position: vectors.Vector2D = vectors.Vector2D(
            int(self.position.x),
            int(self.position.y)
        )
        if self.draw_sprite:
            position = self.compute_position()
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
    