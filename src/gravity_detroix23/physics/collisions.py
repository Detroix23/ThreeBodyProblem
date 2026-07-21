"""
# Three body problem.
src/gravity_detroix23/physics/collisions.py
"""

from gravity_detroix23.physics.vectors import Vector2D
from gravity_detroix23.physics import element
from gravity_detroix23.modules import settings

def collision(
    a: element.Element, 
    b: element.Element, 
    behavior: settings.CollisionsBehavior,
) -> bool:
    """
    Collide two elements and change their velocity by inverting the direction 
    and preserving the actual speed.
    
    To avoid the effect to cancel itself, each `Element` has 
    a list of already collided elements.
    
    Returns:
        `bool`: if collision happened and vector got updated, 
    """
    collision_state: bool = False
    if a not in b.collisions and b not in a.collisions:   
        # Detroix23 collision simplification 4, using a medium vector n, 
        # affected by mass and direction, that reflect the velocity vectors.
        n: Vector2D = a.velocity * a.mass + b.velocity * b.mass
        n.normalize()

        a.velocity =  n * 2 * a.velocity.dot(n) - a.velocity
        b.velocity =  n * 2 * b.velocity.dot(n) - b.velocity

        a.collisions.append(b)
        b.collisions.append(a)
        collision_state = True

        # Check where the elements are going to land.
        distance_min: float = a.size / 2 + b.size / 2
        future_position_a: Vector2D = a.position + a.velocity
        future_position_b: Vector2D = b.position + b.velocity
        future_distance_squared: float = (future_position_a - future_position_b).magnitude2()
        # Try to un-clip.
        if future_distance_squared <= distance_min * distance_min:
            # Collision un-clip.
            v: Vector2D = future_position_b - future_position_a
            d: float = v.magnitude()
            v.normalize()
            displacement: Vector2D = v * (a.size / 2 - d + b.size / 2)
            n_a: float = - b.mass / (a.mass + b.mass)
            n_b: float = a.mass / (a.mass + b.mass)

            a.position += Vector2D(displacement.x, displacement.y) * n_a
            b.position += Vector2D(displacement.x, displacement.y) * n_b
            # print(f"(!) C  Fu: {a.displacement=} {n_a}, {b.displacement=} {n_b}; ")
    
    return collision_state
    