"""
# Gravity.  
src/gravity_detroix23/app/controls.py    
"""
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
	
SPEED_ZERO_THRESHOLD: Final[float] = 0.00001 

class Time:
    """
    Control time and execution speed.
    """
    board: 'Board'
    speed: float
    speed_previous: float

    def __init__(self, board: 'Board') -> None:
        self.board = board
        self.speed = 0.0
        self.speed_previous = 1.0

        return

    def toggle(self) -> None:
        """
        Toggle _on_ or _off_ time pause.
        """
        if abs(self.speed) > SPEED_ZERO_THRESHOLD:
            self.speed_previous = self.speed
            self.speed = 0.0
        else:
            self.speed = self.speed_previous
        
        return
    