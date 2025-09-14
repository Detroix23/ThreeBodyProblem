"""
THREE BODY PROBLEM
collisions.py
"""

from modules.maths_local import *
import modules.element as element
import modules.settings as settings


def collision(a: element.Element, b: element.Element, behaviour: settings.CollisionsBehaviour) -> bool:
    """
    Collide two elements and change their velocity by inverting the direction and preserving the actual speed.
    To avoid the effect to cancel itself, each Elem has a list of already collided elements.
    Return True if collision actually happened, False otherwise
    """
    collision_state: bool = False
    if a not in b.collisions and b not in a.collisions:   
        # Detroix23 collision simplification 4, using a medium vector n, affected by mass and direction, that reflect the velocity vectors.
        n: Vector2D = a.velocity * a.mass + b.velocity * b.mass
        n.normalize()

        a.velocity = ((n * 2) * (a.velocity.dot(n))) - a.velocity
        b.velocity = ((n * 2) * (b.velocity.dot(n))) - b.velocity

        a.collisions.append(b)
        b.collisions.append(a)
        collision_state = True
        # Check where the elems are going to land.
        distance_min = a.size / 2 + b.size / 2
        future_position_a: Vector2D = a.position + a.velocity
        future_position_b: Vector2D = b.position + b.velocity
        future_distance: float = math.sqrt((future_position_a.x - future_position_b.x) ** 2 + (future_position_a.y - future_position_b.y) ** 2)
        # Try to unclip
        if future_distance < distance_min:
            # Collision unclip.
            v: Vector2D = Vector2D(future_position_b.x - future_position_a.x, future_position_b.y - future_position_a.y)
            d: float = v.magnitude
            v.normalize()
            displacement: Vector2D = v * (a.size / 2 - d + b.size / 2)
            n_a: float = - b.mass / (a.mass + b.mass)
            n_b: float = a.mass / (a.mass + b.mass)

            a.displacement = Vector2D(displacement.x, displacement.y) * n_a
            b.displacement = Vector2D(displacement.x, displacement.y) * n_b
            # print(f"! C - Fu: {a.displacement=} {n_a}, {b.displacement=} {n_b}; ")
    return collision_state
    