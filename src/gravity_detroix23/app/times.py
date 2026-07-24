"""
# Gravity.  
src/gravity_detroix23/app/controls.py    
"""
from typing import TYPE_CHECKING, Final

import pyxel

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.modules import scene_objects
    
SPEED_ZERO_THRESHOLD: Final[float] = 0.00001 
SPEED_SCALES: Final[list[float]] = [0.01, 0.1, 0.5, 1.0, 2.0, 4.0]

class Time(scene_objects.Updatable):
    """
    Control time and execution speed.
    """
    board: 'Board'
    speed: float
    paused: bool

    def __init__(self, board: 'Board') -> None:
        self.board = board
        self.speed = 0.0
        self.paused = True

        return

    def toggle(self) -> None:
        """
        Toggle _on_ or _off_ time pause.
        """
        self.paused = not self.paused

        return

    def get_speed(self) -> float:
        """
        Get current time speed for the simulation.
        Returns `0` if `paused`.
        """
        return (0.0
            if self.paused
            else self.speed
        )

    def update(self) -> None:
        """
        Listen to keys to update speed.    
        """
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.board.times.toggle()

        for index in range(len(SPEED_SCALES)):
            key: str = f"KEY_{index + 1}"
            if (
                hasattr(pyxel, key)
                and pyxel.btn(getattr(pyxel, key))
            ):
                self.board.times.speed = SPEED_SCALES[index]
            
        return
    