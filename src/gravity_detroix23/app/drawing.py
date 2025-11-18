"""
# Gravity.
src/gravity/app/drawing.py    
"""
import pyxel

def draw_point(x: int, y: int, color: int) -> None:
    """
    Draw a small square as a point.
    """
    radius: int = 3
    pyxel.rect(x - radius, y - radius, radius * 2, radius * 2, col=color)
