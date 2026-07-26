"""
# Three body problem.
src/gravity_detroix23/physics/collisions.py
"""
import math

from gravity_detroix23.physics import element, vectors
from gravity_detroix23.modules import settings
from gravity_detroix23.physics.vectors import Vector2D


def momentum(
    a: element.Element,
    b: element.Element,
    direction: Vector2D
) -> float:
    """
    Compute the velocity after collision of element `a`.
    Total kinetic energy remains the same in an elastic collision.
    """
    return (
        a.velocity.dot(direction) 
        * (a.mass - b.mass) 
        + b.velocity.dot(direction) 
        * 2 * b.mass
    ) / (a.mass + b.mass)

def collision(
    a: element.Element, 
    b: element.Element, 
    behavior: settings.CollisionsBehavior,
) -> bool:
    """
    Collide two elements and change their velocity by inverting the direction 
    and preserving the actual speed.

    Returns:
        `bool`: if collision happened and vector got updated.
    
    Sources:
    - https://splashkit.io/guides/physics/4-collision-detection-using-vectors/#handling-collisions
    """
    vector: Vector2D = a.get_position() - b.get_position()
    distance2: float = vector.magnitude2()
    radii: float = float(a.size + b.size) / 2.0
    if distance2 > radii * radii:
        return False

    distance: float = math.sqrt(distance2)

    # Direction.
    direction: Vector2D = vector.copy().normalize()

    # Overlap
    overlap: float = max(radii - distance, 0.0) / 2.0
    a.position += overlap * direction
    b.position -= overlap * direction
    
    orthogonal: Vector2D = vectors.orthogonal(direction)


    a.set_velocity(
        orthogonal * a.velocity.dot(orthogonal)
        + direction * momentum(a, b, direction)
    )
    b.set_velocity(
        orthogonal * b.velocity.dot(orthogonal)
        + direction * momentum(b, a, direction)
    )

    return True
    