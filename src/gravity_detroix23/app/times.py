"""
# Gravity.  
src/gravity_detroix23/app/controls.py    
"""
from typing import TYPE_CHECKING, Final, Callable

import pyxel

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.modules import keys
    
SPEED_ZERO_THRESHOLD: Final[float] = 0.00001 
SPEED_SCALES: Final[list[float]] = [0.01, 0.1, 0.5, 1.0, 2.0, 4.0]

class Time(keys.KeySensitive):
    """
    Control time and execution speed.
    """
    board: 'Board'
    speed: float
    paused: bool
    bindings: list[keys.KeyBinding]

    def __init__(self, board: 'Board') -> None:
        self.board = board
        self.speed = 0.0
        self.paused = True
        self.bindings = [
            keys.KeyBinding(
                getattr(pyxel, f"KEY_{index}"),
                f"Time: speed preset {index}",
                self.set_speed_factory(speed),
            )
            for index, speed in enumerate(SPEED_SCALES)
            if hasattr(pyxel, f"KEY_{index}")
        ] + [keys.KeyBinding(
            pyxel.KEY_SPACE,
            "Time: toggle pause",
            lambda: self.board.times.toggle(),
            keys.Trigger.RELEASED,
        )]

        return

    def set_speed_factory(self, value: float) -> Callable[[], None]:
        """
        Create preset to `value` `set_speed` functions.
        """
        return lambda: self.set_speed(value)

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

    def set_speed(self, value: float) -> None:
        """
        Set the variable `speed` to `value`.
        """
        assert value > 0.0
        self.speed = value
        return

    def get_bindings(self) -> list[keys.KeyBinding]:
        return self.bindings
    