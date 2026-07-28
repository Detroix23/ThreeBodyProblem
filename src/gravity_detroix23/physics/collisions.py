"""
# Three body problem.
src/gravity_detroix23/physics/collisions.py
"""
import math

from gravity_detroix23.physics import element, vectors
from gravity_detroix23.physics.vectors import Vector2D


def momentum(
    a: element.Element,
    b: element.Element,
    direction: Vector2D
) -> float:
    """
    Compute the velocity after collision of element `a`.
    Total kinetic energy remains the same in an elastic collision.
    
    From SplashKit:
    ```
    ball_1_momentum = (
        ball_1_collision_dot_product 
        * (ball_1.mass - ball_2.mass) 
        + ball_2_collision_dot_product
        * 2.0f * ball_2.mass
    ) / (ball_1.mass + ball_2.mass);
    ```
    """
    return (
        a.velocity.dot(direction) 
        * (a.mass - b.mass) 
        + b.velocity.dot(direction) 
        * 2.0 * b.mass
    ) / (a.mass + b.mass)

def responses_sum(
    a: element.Element,
    b: element.Element,
    direction: Vector2D,
    orthogonal: Vector2D,
) -> Vector2D:
    """
    Return the sum of the tangential and normal responses.

    Arguments:
        `a`: `Element`: main element;
        `b`: `Element`: secondary element;
        `direction`: `Vector2D`: normalized direction of the collision;
        `orthogonal`: `Vector2D`: collision direction normal vector; 
    
    From SplashKit:
    ```
    ball_1.velocity = vector_add(
        vector_multiply(collision_normal, ball_1_normal_dot_product), 
        vector_multiply(normalized_collision, ball_1_momentum)
    );
    ```
    """
    return (
        orthogonal * a.velocity.dot(orthogonal)
        + direction * momentum(a, b, direction)
    )

def collision(
    a: element.Element, 
    b: element.Element, 
) -> bool:
    """
    Collide two elements and change their velocity by inverting the direction 
    and preserving the actual speed.

    Returns:
        `bool`: if collision happened and vector got updated.
    
    Sources:
    - https://splashkit.io/guides/physics/4-collision-detection-using-vectors/#handling-collisions
    """
    # Distance vector, subtracting `b` to `a`
    vector: Vector2D = a.get_position() - b.get_position()
    distance2: float = vector.magnitude2()
    radii: float = float(a.size + b.size) / 2.0
    if distance2 > radii * radii:
        return False

    distance: float = math.sqrt(distance2)

    # Normalized tangent collision vector, 
    # representing the direction from `b` to `a`.
    direction: Vector2D = vector.copy().normalize()

    # Overlap.z
    overlap: float = (radii - distance) / 2.0
    a.position += overlap * direction
    b.position -= overlap * direction

    # Collision normal vector, orthogonal to `direction`.
    orthogonal: Vector2D = vectors.orthogonal(direction)

    print(f"(?) physics.collisions.collision(a, b) Before: ")
    print(f"- v_a = {a.velocity}")
    print(f"- v_b = {b.velocity}")
    a.set_velocity(responses_sum(a, b, direction, orthogonal))
    b.set_velocity(responses_sum(b, a, direction, orthogonal))

    print("After: ")
    print(f"- v_a = {a.velocity}")
    print(f"- v_b = {b.velocity}")

    #exit(-1)

    return True
    