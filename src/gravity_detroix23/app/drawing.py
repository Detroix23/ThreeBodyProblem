"""
# Gravity.
src/gravity/app/drawing.py    
"""
import pyxel

from gravity_detroix23.modules.types import Number

def draw_point(x: Number, y: Number, color: int, radius: int = 3) -> None:
    """
    Draw a small square as a point.
    """
    pyxel.rect(x - radius, y - radius, radius * 2, radius * 2, col=color)
