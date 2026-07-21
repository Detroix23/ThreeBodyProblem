"""
# Gravity.
src/gravity_detroix23/physics/forces.py
"""

def gravity(
    distance: float,
    mass: float,
    gravitational_constant: float,
    exponent_softener: float = 0.0,
) -> float:
    """
    Returns the `float` value of the gravitational force from an object:
    - `distance` away;
    - with `mass`. 
    """
    return (
        (gravitational_constant * mass) 
        / (distance ** (2 + exponent_softener))
    )
