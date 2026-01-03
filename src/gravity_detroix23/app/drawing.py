"""
# Gravity.
src/gravity/app/drawing.py    
"""
import pyxel

def draw_point(x: int, y: int, color: int, radius: int = 3) -> None:
    """
    Draw a small square as a point.
    """
    pyxel.rect(x - radius, y - radius, radius * 2, radius * 2, col=color)
