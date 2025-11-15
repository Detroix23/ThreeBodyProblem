"""
THREE BODY PROBLEM.
drawing_utils.py
"""
import pyxel

def draw_point(x: int, y: int, color: int) -> None:
    """
    Draw a point as a small square.
    """
    radius: int = 3
    pyxel.rect(x - radius, y - radius, radius * 2, radius * 2, col=color)