"""
# Gravity.
src/gravity_detroix23/physics/element.py
"""
import math
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app.board import Board 

from gravity_detroix23.modules import defaults, entity, settings
from gravity_detroix23.physics import trails, forces, collisions
from gravity_detroix23.app import drawing
from gravity_detroix23.physics.vectors import Vector2D

class Element(entity.Entity):
    """
    Define a stellar element
    """
    CHECK_RADIUS: int = 100
    SPRITE_POSITION: Vector2D = Vector2D(16.0, 0.0)
    SPRITE_SIZE: Vector2D = Vector2D(16.0, 16.0)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = defaults.SPRITE_COLKEY
    SPRITE_SIZE_FACTOR: float = 1/16

    board: 'Board'
    mass: float
    position: Vector2D
    velocity: Vector2D
    acceleration: Vector2D
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
        position: Vector2D, 
        velocity: Vector2D,
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
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector2D.null()
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
            f"{self.name}, mass={self.mass} position={self.position}, "
            f"velocity={self.velocity}, acceleration={self.acceleration})"
        )

    def __repr__(self) -> str:
        return (
            f"Element(name={self.name}, mass={self.mass}, position={self.position},"
            f"velocity={self.velocity}, acceleration={self.acceleration}, "
            f"color={self.color}, size={self.size})"
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
    
    def gravitational_force_from(self, target: 'Element') -> Vector2D:
        """
        Find the gravitational force vector between `self` and `target`.
        """
        # Direction
        way: int = 1
        normal: Vector2D = Vector2D(
            target.position.x - self.position.x,
            target.position.y - self.position.y,
        )
        normal.normalize()
        
        # Distance.
        distance2: float = self.distance2(target)
        # Limit artificially distance and prevent division by 0
        distance_min: float = (self.size + target.size + 2) / 2
        distance: float = (
            distance_min
            if distance2 < distance_min * distance_min
            else math.sqrt(distance2)
        )

        # F force value.
        force: float = forces.gravity(
            distance, 
            target.mass,
            self.board.gravitational_constant,
            self.board.exponent_softener,
        )
        
        # Force vector
        vector_force: Vector2D = normal * force * way
        
        return vector_force

    def interaction(self, target: Element) -> None:
        """
        Manage the potential side-effects of an `interaction` between
        `self` and `element`.  
        """
        distance2: float = self.distance2(target)
        if (
            distance2 <= (self.size + target.size) * (self.size + target.size) / 4
            and self.board.collisions is not settings.CollisionsBehavior.NONE, 
        ):
            collisions.collision(
                self, 
                target, 
                behavior=self.board.collisions,
            )
    
        return

    def update(self) -> None:
        """
        Move the element, according to force vector at a scale (mass) and checking collision.
        """ 
        net_force: Vector2D = Vector2D.null()
        for element in self.board.system.values():
            if self != element:
                net_force += self.gravitational_force_from(element)
                self.interaction(element)

        # Apply force.
        dt: float = self.board.times.speed
        
        self.acceleration.add( 
            net_force
            / (self.mass * self.board.mass_softener)
        )
        self.velocity.add(
            self.acceleration * dt
        )
        self.position.add(
            self.velocity * self.board.times.speed
            + 0.5 * self.acceleration * dt * dt
        )

        # Update trail.
        if self.trail and not self.position.is_close(self.trail.first, 1):
            self.trail.push(self.position.copy())


        self.collisions = list()

        return
    
    def compute_position(self) -> Vector2D:
        """
        Get the on-screen position, transformed by the `camera`.
        """    
        return self.board.camera.transform(
             self.position 
            - Vector2D.duplicate(self.SPRITE_SIZE_FACTOR) * 2
        )

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        # Draw on computed values.
        size: int = int(self.size)
        position: Vector2D = Vector2D(
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

        return