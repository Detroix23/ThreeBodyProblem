"""
THREE BODY PROBLEM
camera.py
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import modules.simulation as simulation
from modules.maths_local import *
import modules.element as element


class Camera:
    def __init__(self, simulation: simulation.Board) -> None:
        self.simulation: simulation.Board = simulation
        self.position: Vector2D = Vector2D(0, 0)
        self.zoom: float = 1.0

    def follow_element(self, elem: element.Element) -> None:
        self.position.x = elem.position.x - self.simulation.width / 2
        self.position.y = elem.position.y - self.simulation.height / 2
